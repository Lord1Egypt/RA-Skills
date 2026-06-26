/**
 * form_filler.mjs — Generic form filling
 * Config-driven: answers loaded from answers.json
 * Returns list of unknown required fields
 *
 * Performance: uses a single evaluate() to snapshot all form state from the DOM,
 * does answer matching locally in Node, then only makes CDP calls to fill/click.
 */
import { writeFileSync, renameSync } from 'fs';
import {
  DEFAULT_YEARS_EXPERIENCE, DEFAULT_DESIRED_SALARY,
  MINIMUM_SALARY_FACTOR, DEFAULT_SKILL_RATING,
  LINKEDIN_EASY_APPLY_MODAL_SELECTOR, FORM_PATTERN_MAX_LENGTH,
  AUTOCOMPLETE_WAIT, AUTOCOMPLETE_TIMEOUT, ANTHROPIC_API_URL
} from './constants.mjs';

/**
 * Normalize answers from either format:
 *   Object: { "question": "answer" }  ->  [{ pattern: "question", answer: "answer" }]
 *   Array:  [{ pattern, answer }]     ->  as-is
 */
function normalizeAnswers(answers) {
  if (!answers) return [];
  if (Array.isArray(answers)) return answers;
  if (typeof answers === 'object') {
    return Object.entries(answers).map(([pattern, answer]) => ({ pattern, answer: String(answer) }));
  }
  return [];
}

/**
 * Extract label text from a DOM node. Runs inside evaluate().
 * Checks: label[for], aria-label, aria-labelledby, ancestor label, placeholder, name.
 */
function extractLabel(node) {
  const id = node.id;
  const forLabel = id ? document.querySelector(`label[for="${id}"]`)?.textContent?.trim() : '';
  const ariaLabel = node.getAttribute('aria-label') || '';
  const ariaLabelledBy = node.getAttribute('aria-labelledby');
  const linked = ariaLabelledBy ? document.getElementById(ariaLabelledBy)?.textContent?.trim() : '';

  let ancestorLabel = '';
  if (!forLabel && !ariaLabel && !linked) {
    let parent = node.parentElement;
    for (let i = 0; i < 5 && parent; i++) {
      const lbl = parent.querySelector('label');
      if (lbl) {
        ancestorLabel = lbl.textContent?.trim() || '';
        break;
      }
      parent = parent.parentElement;
    }
  }

  let raw = forLabel || ariaLabel || linked || ancestorLabel || node.placeholder || node.name || '';
  raw = raw.replace(/\s+/g, ' ').replace(/\s*\*\s*$/, '').replace(/\s*Required\s*$/i, '').trim();
  // Deduplicate repeated label text (LinkedIn renders label text twice)
  if (raw.length > 8) {
    for (let len = Math.ceil(raw.length / 2); len >= 4; len--) {
      const candidate = raw.slice(0, len);
      if (raw.startsWith(candidate + candidate)) {
        raw = candidate.trim();
        break;
      }
    }
  }
  return raw;
}

/**
 * Check if a node is required. Runs inside evaluate().
 */
function checkRequired(node) {
  if (node.required || node.getAttribute('required') !== null) return true;
  if (node.getAttribute('aria-required') === 'true') return true;
  const id = node.id;
  if (id) {
    const label = document.querySelector(`label[for="${id}"]`);
    if (label && label.textContent.includes('*')) return true;
  }
  let parent = node.parentElement;
  for (let i = 0; i < 5 && parent; i++) {
    const lbl = parent.querySelector('label');
    if (lbl && lbl.textContent.includes('*')) return true;
    const reqSpan = parent.querySelector('[class*="required"], .artdeco-text-input--required');
    if (reqSpan) return true;
    parent = parent.parentElement;
  }
  return false;
}

/**
 * Normalize a fieldset legend, same logic as extractLabel dedup.
 */
function normalizeLegend(el) {
  let raw = (el.textContent || '').replace(/\s+/g, ' ').replace(/\s*\*\s*$/, '').replace(/\s*Required\s*$/i, '').trim();
  if (raw.length > 8) {
    for (let len = Math.ceil(raw.length / 2); len >= 4; len--) {
      const candidate = raw.slice(0, len);
      if (raw.startsWith(candidate + candidate)) { raw = candidate.trim(); break; }
    }
  }
  return raw;
}

export class FormFiller {
  constructor(profile, answers, opts = {}) {
    this.profile = profile;
    this.answers = normalizeAnswers(answers); // [{ pattern, answer }]
    this.apiKey = opts.apiKey || null;
    this.answersPath = opts.answersPath || null;
    this.jobContext = opts.jobContext || {};
  }

  saveAnswer(pattern, answer) {
    if (!pattern || !answer) return;
    const existing = this.answers.findIndex(a => a.pattern === pattern);
    if (existing >= 0) return;
    this.answers.push({ pattern, answer });
    if (this.answersPath) {
      try {
        const tmp = this.answersPath + '.tmp';
        writeFileSync(tmp, JSON.stringify(this.answers, null, 2));
        renameSync(tmp, this.answersPath);
      } catch { /* best effort */ }
    }
  }

  answerFor(label) {
    if (!label) return null;
    const l = label.toLowerCase();

    // Check custom answers first
    for (const entry of this.answers) {
      try {
        if (entry.pattern.length > FORM_PATTERN_MAX_LENGTH) throw new Error('pattern too long');
        const re = new RegExp(entry.pattern, 'i');
        if (re.test(l)) return String(entry.answer);
      } catch {
        if (l.includes(entry.pattern.toLowerCase())) return String(entry.answer);
      }
    }

    const p = this.profile;

    // Contact
    if (l.includes('first name') && !l.includes('last')) return p.name?.first || null;
    if (l.includes('last name')) return p.name?.last || null;
    if (l.includes('full name') || l === 'name') {
      const first = p.name?.first;
      const last = p.name?.last;
      return (first && last) ? `${first} ${last}` : null;
    }
    if (l.includes('email')) return p.email || null;
    if (l.includes('phone') || l.includes('mobile')) return p.phone || null;
    if (l.includes('city') && !l.includes('remote')) return p.location?.city || null;
    if (l.includes('zip') || l.includes('postal')) return p.location?.zip || null;
    if (l.includes('country code') || l.includes('phone country')) return 'United States (+1)';
    if (l.includes('country')) return p.location?.country || null;
    if (l.includes('state') && !l.includes('statement')) return p.location?.state || null;
    if (l.includes('linkedin')) return p.linkedin_url || null;
    if (l.includes('website') || l.includes('portfolio')) return p.linkedin_url || null;
    if (l.includes('currently located') || l.includes('current location') || l.includes('where are you')) {
      return `${p.location?.city || ''}, ${p.location?.state || ''}`.trim().replace(/^,\s*|,\s*$/, '');
    }
    if (l.includes('hear about') || l.includes('how did you find') || l.includes('how did you hear')) return 'LinkedIn';

    // Work auth
    if (l.includes('sponsor') || l.includes('visa')) return p.work_authorization?.requires_sponsorship ? 'Yes' : 'No';
    if (l.includes('relocat')) return p.willing_to_relocate ? 'Yes' : 'No';
    if (l.includes('authoriz') || l.includes('eligible') || l.includes('legally') || l.includes('work in the u') || l.includes('right to work')) {
      return p.work_authorization?.authorized ? 'Yes' : 'No';
    }
    if (l.includes('remote') && (l.includes('willing') || l.includes('comfortable') || l.includes('able to'))) return 'Yes';

    // Experience
    if (l.includes('year') && (l.includes('experienc') || l.includes('exp') || l.includes('work'))) {
      if (l.includes('enterprise') || l.includes('b2b')) return '5';
      if (l.includes('crm') || l.includes('salesforce') || l.includes('hubspot') || l.includes('database')) return '7';
      if (l.includes('cold') || l.includes('outbound') || l.includes('prospecting')) return '5';
      if (l.includes('sales') || l.includes('revenue') || l.includes('quota') || l.includes('account')) return '7';
      if (l.includes('saas') || l.includes('software') || l.includes('tech')) return '7';
      if (l.includes('manag') || l.includes('leadership')) return '3';
      return String(p.years_experience || DEFAULT_YEARS_EXPERIENCE);
    }

    // 1-10 scale
    if (l.includes('1 - 10') || l.includes('1-10') || l.includes('scale of 1') || l.includes('rate your')) {
      if (l.includes('cold') || l.includes('outbound') || l.includes('prospecting')) return '9';
      if (l.includes('sales') || l.includes('selling') || l.includes('revenue') || l.includes('gtm')) return '9';
      if (l.includes('enterprise') || l.includes('b2b')) return '9';
      if (l.includes('technical') || l.includes('engineering')) return '7';
      if (l.includes('crm') || l.includes('salesforce')) return '8';
      return DEFAULT_SKILL_RATING;
    }

    // Compensation
    if (l.includes('salary') || l.includes('compensation') || l.includes('expected pay')) return String(p.desired_salary || '');
    if (l.includes('minimum') && l.includes('salary')) return String(Math.round((p.desired_salary || DEFAULT_DESIRED_SALARY) * MINIMUM_SALARY_FACTOR));

    // Dates
    if (l.includes('start date') || l.includes('when can you start') || l.includes('available to start')) return 'Immediately';
    if (l.includes('notice period')) return '2 weeks';

    // Education
    if (l.includes('degree') || l.includes('bachelor')) return 'No';

    // Cover letter
    if (l.includes('cover letter') || l.includes('additional info') || l.includes('tell us') ||
        l.includes('why do you') || l.includes('about yourself') || l.includes('message to')) {
      return p.cover_letter || '';
    }

    return null;
  }

  isHoneypot(label) {
    const l = (label || '').toLowerCase();
    return l.includes('digit code') || l.includes('secret word') || l.includes('not apply on linkedin') ||
           l.includes('best way to apply') || l.includes('hidden code') || l.includes('passcode');
  }

  // Keep these for external callers (test scripts etc)
  async getLabel(el) {
    return await el.evaluate(extractLabel).catch(() => '');
  }

  async isRequired(el) {
    return await el.evaluate(checkRequired).catch(() => false);
  }

  async aiAnswerFor(label, opts = {}) {
    if (!this.apiKey) return null;

    const savedAnswers = this.answers.map(a => `Q: "${a.pattern}" -> A: "${a.answer}"`).join('\n');
    const optionsHint = opts.options?.length ? `\nAvailable options: ${opts.options.join(', ')}` : '';

    const systemPrompt = `You are helping a job candidate fill out application forms. You have access to their profile and previously answered questions.

Rules:
- If this question is a variation of a previously answered question, return the SAME answer
- For yes/no or multiple choice, return ONLY the exact option text
- For short-answer fields, be brief and direct (1 line)
- Use first person
- Never make up facts
- Just the answer text — no preamble, no explanation, no quotes`;

    const userPrompt = `Candidate: ${this.profile.name?.first} ${this.profile.name?.last}
Location: ${this.profile.location?.city}, ${this.profile.location?.state}
Years experience: ${this.profile.years_experience || 7}
Applying for: ${this.jobContext.title || 'a role'} at ${this.jobContext.company || 'a company'}

Previously answered questions:
${savedAnswers || '(none yet)'}

New question: "${label}"${optionsHint}

Answer:`;

    try {
      const res = await fetch(ANTHROPIC_API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': this.apiKey,
          'anthropic-version': '2023-06-01',
        },
        body: JSON.stringify({
          model: 'claude-sonnet-4-6',
          max_tokens: 256,
          system: systemPrompt,
          messages: [{ role: 'user', content: userPrompt }],
        }),
      });
      if (!res.ok) return null;
      const data = await res.json();
      const answer = data.content?.[0]?.text?.trim() || null;
      if (answer) console.log(`    [AI] "${label}" -> "${answer}"`);
      return answer;
    } catch {
      return null;
    }
  }

  async selectOptionFuzzy(sel, answer) {
    const exactWorked = await sel.selectOption({ label: answer }).then(() => true).catch(() => false);
    if (exactWorked) return;

    // Batch-read all option texts in one evaluate instead of per-element textContent() calls
    const target = answer.trim().toLowerCase();
    const optTexts = await sel.evaluate(el =>
      Array.from(el.options).map(o => o.textContent?.trim() || '')
    ).catch(() => []);

    const exact = optTexts.find(t => t.toLowerCase() === target);
    if (exact) { await sel.selectOption({ label: exact }).catch(() => {}); return; }

    const substring = optTexts.find(t => t.toLowerCase().includes(target));
    if (substring) { await sel.selectOption({ label: substring }).catch(() => {}); return; }

    await sel.selectOption({ value: answer }).catch(() => {});
  }

  async selectAutocomplete(page, container) {
    const selectors = '[role="option"], [role="listbox"] li, ul[class*="autocomplete"] li';
    const option = await container.waitForSelector(selectors, {
      timeout: AUTOCOMPLETE_TIMEOUT, state: 'visible',
    }).catch(() => {
      return page.waitForSelector(selectors, {
        timeout: AUTOCOMPLETE_TIMEOUT, state: 'visible',
      }).catch(() => null);
    });
    if (option) {
      await option.click().catch(() => {});
      await page.waitForTimeout(AUTOCOMPLETE_WAIT);
    }
  }

  /**
   * Snapshot all form fields from the DOM in a single evaluate() call.
   * Returns a plain JSON object describing every field, avoiding per-element CDP round-trips.
   */
  async _snapshotFields(container) {
    return await container.evaluate((rootOrUndefined) => {
      // When container is an ElementHandle, root is the element.
      // When container is a Page, root is undefined — use document.
      const root = rootOrUndefined || document;

      function _extractLabel(node) {
        const id = node.id;
        const forLabel = id ? document.querySelector('label[for="' + id + '"]')?.textContent?.trim() : '';
        const ariaLabel = node.getAttribute('aria-label') || '';
        const ariaLabelledBy = node.getAttribute('aria-labelledby');
        const linked = ariaLabelledBy ? document.getElementById(ariaLabelledBy)?.textContent?.trim() : '';

        let ancestorLabel = '';
        if (!forLabel && !ariaLabel && !linked) {
          let parent = node.parentElement;
          for (let i = 0; i < 5 && parent; i++) {
            const lbl = parent.querySelector('label');
            if (lbl) {
              ancestorLabel = lbl.textContent?.trim() || '';
              break;
            }
            parent = parent.parentElement;
          }
        }

        let raw = forLabel || ariaLabel || linked || ancestorLabel || node.placeholder || node.name || '';
        raw = raw.replace(/\s+/g, ' ').replace(/\s*\*\s*$/, '').replace(/\s*Required\s*$/i, '').trim();
        if (raw.length > 8) {
          for (let len = Math.ceil(raw.length / 2); len >= 4; len--) {
            const candidate = raw.slice(0, len);
            if (raw.startsWith(candidate + candidate)) {
              raw = candidate.trim();
              break;
            }
          }
        }
        return raw;
      }

      function _checkRequired(node) {
        if (node.required || node.getAttribute('required') !== null) return true;
        if (node.getAttribute('aria-required') === 'true') return true;
        const id = node.id;
        if (id) {
          const label = document.querySelector('label[for="' + id + '"]');
          if (label && label.textContent.includes('*')) return true;
        }
        let parent = node.parentElement;
        for (let i = 0; i < 5 && parent; i++) {
          const lbl = parent.querySelector('label');
          if (lbl && lbl.textContent.includes('*')) return true;
          const reqSpan = parent.querySelector('[class*="required"], .artdeco-text-input--required');
          if (reqSpan) return true;
          parent = parent.parentElement;
        }
        return false;
      }

      function _normalizeLegend(el) {
        let raw = (el.textContent || '').replace(/\s+/g, ' ').replace(/\s*\*\s*$/, '').replace(/\s*Required\s*$/i, '').trim();
        if (raw.length > 8) {
          for (let len = Math.ceil(raw.length / 2); len >= 4; len--) {
            const candidate = raw.slice(0, len);
            if (raw.startsWith(candidate + candidate)) { raw = candidate.trim(); break; }
          }
        }
        return raw;
      }

      function isVisible(el) {
        if (!el.offsetParent && el.style.position !== 'fixed') return false;
        const style = window.getComputedStyle(el);
        return style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0';
      }

      const result = {
        resumeRadios: [],
        hasFileInput: false,
        inputs: [],
        textareas: [],
        fieldsets: [],
        selects: [],
        checkboxes: [],
      };

      // Resume radios
      const resumeInputs = root.querySelectorAll('input[type="radio"][aria-label*="resume"], input[type="radio"][aria-label*="Resume"]');
      let resumeChecked = false;
      resumeInputs.forEach((r, i) => {
        if (r.checked) resumeChecked = true;
        result.resumeRadios.push({ index: i, checked: r.checked });
      });
      result.resumeChecked = resumeChecked;

      // File input
      result.hasFileInput = !!root.querySelector('input[type="file"]');

      // Tag each element with data-claw-idx so we can reliably find it later
      // (avoids fragile positional index matching between snapshot and querySelectorAll)
      let idx = 0;

      // Text / number / url / email / tel inputs
      const inputEls = root.querySelectorAll('input[type="text"], input[type="number"], input[type="url"], input[type="email"], input[type="tel"]');
      inputEls.forEach((inp) => {
        if (!isVisible(inp)) return;
        const tag = 'inp-' + (idx++);
        inp.setAttribute('data-claw-idx', tag);
        result.inputs.push({ tag, label: _extractLabel(inp), value: inp.value || '', placeholder: inp.placeholder || '', required: _checkRequired(inp), type: inp.type });
      });

      // Textareas
      const taEls = root.querySelectorAll('textarea');
      taEls.forEach((ta) => {
        if (!isVisible(ta)) return;
        const tag = 'ta-' + (idx++);
        ta.setAttribute('data-claw-idx', tag);
        result.textareas.push({ tag, label: _extractLabel(ta), value: ta.value || '', placeholder: ta.placeholder || '', required: _checkRequired(ta) });
      });

      // Fieldsets
      const fsEls = root.querySelectorAll('fieldset');
      fsEls.forEach((fs) => {
        const legend = fs.querySelector('legend');
        if (!legend) return;
        const leg = _normalizeLegend(legend);
        if (!leg) return;

        const tag = 'fs-' + (idx++);
        fs.setAttribute('data-claw-idx', tag);

        const checkboxes = fs.querySelectorAll('input[type="checkbox"]');
        const isCheckboxGroup = checkboxes.length > 0;
        const radios = fs.querySelectorAll('input[type="radio"]');
        let anyChecked = false;
        radios.forEach(r => { if (r.checked) anyChecked = true; });
        checkboxes.forEach(c => { if (c.checked) anyChecked = true; });

        const options = [];
        fs.querySelectorAll('label').forEach(lbl => {
          const t = (lbl.textContent || '').trim();
          if (t) options.push(t);
        });

        const selectInFs = fs.querySelector('select');
        const selectOptions = [];
        if (selectInFs) {
          selectInFs.querySelectorAll('option').forEach(opt => {
            const t = (opt.textContent || '').trim();
            if (t && !/^select/i.test(t)) selectOptions.push(t);
          });
        }

        result.fieldsets.push({
          tag, legend: leg, isCheckboxGroup,
          anyChecked, options, hasSelect: !!selectInFs, selectOptions,
        });
      });

      // Selects (standalone)
      const selEls = root.querySelectorAll('select');
      selEls.forEach((sel) => {
        if (!isVisible(sel)) return;
        const inFieldset = !!sel.closest('fieldset')?.querySelector('legend');
        const tag = 'sel-' + (idx++);
        sel.setAttribute('data-claw-idx', tag);
        result.selects.push({
          tag, label: _extractLabel(sel), value: sel.value || '',
          selectedText: sel.options[sel.selectedIndex]?.textContent?.trim() || '',
          required: _checkRequired(sel), inFieldset,
          options: Array.from(sel.querySelectorAll('option'))
            .map(o => (o.textContent || '').trim())
            .filter(t => t && !/^select/i.test(t)),
        });
      });

      // Checkboxes (standalone)
      const cbEls = root.querySelectorAll('input[type="checkbox"]');
      cbEls.forEach((cb) => {
        if (!isVisible(cb)) return;
        if (cb.closest('fieldset')?.querySelector('legend')) return;
        const tag = 'cb-' + (idx++);
        cb.setAttribute('data-claw-idx', tag);
        result.checkboxes.push({ tag, label: _extractLabel(cb), checked: cb.checked });
      });

      return result;
    }).catch(() => null);
  }

  /**
   * Fill all fields in a container (page or modal element).
   * Uses _snapshotFields() to batch-read all DOM state in one call,
   * then only makes individual CDP calls for elements that need action.
   * Returns array of unknown required field labels.
   */
  async fill(page, resumePath) {
    const unknown = [];
    const container = await page.$(LINKEDIN_EASY_APPLY_MODAL_SELECTOR) || page;

    // Single DOM snapshot — all labels, values, visibility, required status
    const snap = await this._snapshotFields(container);
    if (!snap) return unknown;

    // Log field counts for debugging
    const counts = [snap.inputs.length && `${snap.inputs.length} inputs`, snap.textareas.length && `${snap.textareas.length} textareas`, snap.fieldsets.length && `${snap.fieldsets.length} fieldsets`, snap.selects.length && `${snap.selects.length} selects`, snap.checkboxes.length && `${snap.checkboxes.length} checkboxes`].filter(Boolean);
    if (counts.length > 0) console.log(`    [fill] ${counts.join(', ')}`);

    // Helper: find element by data-claw-idx tag
    const byTag = (tag) => container.$(`[data-claw-idx="${tag}"]`);

    // --- Resume ---
    if (snap.resumeRadios.length > 0 && !snap.resumeChecked) {
      const radios = await container.$$('input[type="radio"][aria-label*="resume"], input[type="radio"][aria-label*="Resume"]');
      if (radios[0]) await radios[0].click().catch(() => {});
    } else if (snap.resumeRadios.length === 0 && snap.hasFileInput && resumePath) {
      const fileInput = await container.$('input[type="file"]');
      if (fileInput) await fileInput.setInputFiles(resumePath).catch(() => {});
    }

    // --- Inputs (text/number/url/email/tel) ---
    for (const field of snap.inputs) {
      const lbl = field.label;
      const ll = lbl.toLowerCase();

      // Phone — always overwrite
      if (ll.includes('phone') || ll.includes('mobile')) {
        const el = await byTag(field.tag);
        if (!el) continue;
        await el.click({ clickCount: 3 }).catch(() => {});
        await el.fill(this.profile.phone || '').catch(() => {});
        continue;
      }

      if (!lbl) continue;
      if (field.value?.trim()) continue;
      if (this.isHoneypot(lbl)) return [{ label: lbl, honeypot: true }];

      // Date fields — detect by placeholder format (e.g. "MM/DD/YYYY")
      const ph = (field.placeholder || '').toUpperCase();
      if (ph.includes('MM') && ph.includes('DD') && ph.includes('YYYY')) {
        const now = new Date();
        const dateStr = `${String(now.getMonth() + 1).padStart(2, '0')}/${String(now.getDate()).padStart(2, '0')}/${now.getFullYear()}`;
        const el = await byTag(field.tag);
        if (el) await el.fill(dateStr).catch(() => {});
        continue;
      }

      const formatHint = field.placeholder ? `(format: ${field.placeholder})` : '';
      let answer = this.answerFor(lbl);
      if (!answer && field.required) {
        answer = await this.aiAnswerFor(formatHint ? `${lbl} ${formatHint}` : lbl);
        if (answer) this.saveAnswer(lbl, answer);
      }
      if (answer && answer !== this.profile.cover_letter) {
        const el = await byTag(field.tag);
        if (!el) continue;
        await el.fill(String(answer)).catch(() => {});
        if (ll.includes('city') || ll.includes('location') || ll.includes('located')) {
          await this.selectAutocomplete(page, container);
        }
      } else if (field.required) {
        unknown.push(lbl);
      }
    }

    // --- Textareas ---
    for (const field of snap.textareas) {
      if (field.value?.trim()) continue;
      const taFormatHint = field.placeholder ? `(format: ${field.placeholder})` : '';
      let answer = this.answerFor(field.label);
      if (!answer && field.required) {
        answer = await this.aiAnswerFor(taFormatHint ? `${field.label} ${taFormatHint}` : field.label);
        if (answer) this.saveAnswer(field.label, answer);
      }
      if (answer) {
        const el = await byTag(field.tag);
        if (el) await el.fill(answer).catch(() => {});
      } else if (field.required) {
        unknown.push(field.label);
      }
    }

    // --- Fieldsets (radios and checkbox groups) ---
    for (const field of snap.fieldsets) {
      if (!field.isCheckboxGroup && field.anyChecked) continue;

      let answer = this.answerFor(field.legend);
      if (answer && field.options.length > 0) {
        const ansLower = answer.toLowerCase();
        const matches = field.options.some(o =>
          o.toLowerCase() === ansLower || o.toLowerCase().includes(ansLower) || ansLower.includes(o.toLowerCase())
        );
        if (!matches) answer = null;
      }
      if (!answer) {
        answer = await this.aiAnswerFor(field.legend, { options: field.options });
        if (answer) this.saveAnswer(field.legend, answer);
      }
      if (answer) {
        const fs = await byTag(field.tag);
        if (!fs) continue;
        const labels = await fs.$$('label');
        if (field.isCheckboxGroup) {
          const selections = answer.split(',').map(s => s.trim().toLowerCase());
          for (const lbl of labels) {
            const text = (await lbl.textContent().catch(() => '') || '').trim();
            if (selections.some(s => text.toLowerCase() === s || text.toLowerCase().includes(s))) {
              await lbl.click().catch(() => {});
            }
          }
        } else {
          let clicked = false;
          for (const lbl of labels) {
            const text = (await lbl.textContent().catch(() => '') || '').trim();
            if (text.toLowerCase() === answer.toLowerCase() ||
                text.toLowerCase().startsWith(answer.toLowerCase())) {
              await lbl.click().catch(() => {});
              clicked = true;
              break;
            }
          }
          if (clicked) {
            const nowChecked = await fs.$('input:checked');
            if (!nowChecked) {
              const radios = await fs.$$('input[type="radio"]');
              for (const radio of radios) {
                const val = await radio.evaluate(el => el.value || el.nextSibling?.textContent?.trim() || '').catch(() => '');
                if (val.toLowerCase() === answer.toLowerCase() ||
                    val.toLowerCase().startsWith(answer.toLowerCase())) {
                  await radio.click({ force: true }).catch(() => {});
                  break;
                }
              }
            }
          }
          if (!clicked || !(await fs.$('input:checked'))) {
            if (field.hasSelect) {
              const sel = await fs.$('select');
              if (sel) await this.selectOptionFuzzy(sel, answer);
            }
          }
        }
      } else {
        unknown.push(field.legend);
      }
    }

    // --- Selects (standalone) ---
    for (const field of snap.selects) {
      if (field.inFieldset) continue;

      const existing = field.selectedText || field.value || '';
      if (existing && !/^select an? /i.test(existing)) continue;

      let answer = this.answerFor(field.label);
      if (answer && field.options.length > 0) {
        const ansLower = answer.toLowerCase();
        const matches = field.options.some(o =>
          o.toLowerCase() === ansLower || o.toLowerCase().includes(ansLower) || ansLower.includes(o.toLowerCase())
        );
        if (!matches) answer = null;
      }
      if (!answer) {
        const ll = field.label.toLowerCase();
        if (ll.includes('race') || ll.includes('ethnicity') || ll.includes('gender') ||
            ll.includes('veteran') || ll.includes('disability') || ll.includes('identification')) {
          const declineOpt = field.options.find(t => /prefer not|decline|do not wish|i don/i.test(t));
          if (declineOpt) {
            const sel = await byTag(field.tag);
            if (sel) await sel.selectOption({ label: declineOpt }).catch(() => {});
          }
          continue;
        }
        if (field.required) {
          answer = await this.aiAnswerFor(field.label, { options: field.options });
          if (answer) {
            this.saveAnswer(field.label, answer);
          } else {
            unknown.push({ label: field.label, type: 'select', options: field.options });
            continue;
          }
        }
      }
      if (answer) {
        const sel = await byTag(field.tag);
        if (sel) await this.selectOptionFuzzy(sel, answer);
      }
    }

    // --- Checkboxes (standalone) ---
    for (const field of snap.checkboxes) {
      if (field.checked) continue;
      const ll = field.label.toLowerCase();
      if (ll.includes('confirm') || ll.includes('agree') || ll.includes('consent')) {
        const el = await byTag(field.tag);
        if (el) await el.check().catch(() => {});
      }
    }

    return unknown;
  }
}

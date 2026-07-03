'use strict';

var { getHubUrl, buildHubHeaders, buildNodeScopedHubHeaders, getNodeId } = require('./a2aProtocol');
var { hubFetch } = require('./hubFetch');

function buildSkillStoreHeaders() {
  var buildHeaders = buildNodeScopedHubHeaders || buildHubHeaders;
  return buildHeaders();
}

/**
 * Sanitize a raw gene id into a human-readable kebab-case skill name.
 * Returns null if the name is unsalvageable (pure numbers, tool name, etc.).
 */
function sanitizeSkillName(rawName) {
  var name = rawName.replace(/[\r\n]+/g, '-').replace(/^gene_distilled_/, '').replace(/^gene_/, '').replace(/_/g, '-');
  // Strip ALL embedded timestamps (10+ digit sequences) anywhere in the name
  name = name.replace(/-?\d{10,}-?/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '');
  if (/^\d{8,}/.test(name) || /^(cursor|vscode|vim|emacs|windsurf|copilot|cline|codex)[-]?\d*$/i.test(name)) {
    return null;
  }
  if (name.replace(/[-]/g, '').length < 6) return null;
  return name;
}

/**
 * Derive a Title Case display name from a kebab-case skill name.
 * "retry-with-backoff" -> "Retry With Backoff"
 */
function toTitleCase(kebabName) {
  return kebabName.split('-').map(function (w) {
    if (!w) return '';
    return w.charAt(0).toUpperCase() + w.slice(1);
  }).join(' ');
}

/**
 * Derive fallback name words from gene signals/summary when id is not usable.
 */
function deriveFallbackName(gene) {
  var fallbackWords = [];
  var STOP = new Set(['the', 'and', 'for', 'with', 'from', 'that', 'this', 'into', 'when', 'are', 'was', 'has', 'had', 'not', 'but', 'its']);
  if (Array.isArray(gene.signals_match)) {
    gene.signals_match.slice(0, 3).forEach(function (s) {
      String(s).toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim().split(/\s+/).forEach(function (w) {
        if (w.length >= 3 && !STOP.has(w) && fallbackWords.length < 5) fallbackWords.push(w);
      });
    });
  }
  if (fallbackWords.length < 2 && gene.summary) {
    String(gene.summary).toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim().split(/\s+/).forEach(function (w) {
      if (w.length >= 3 && !STOP.has(w) && fallbackWords.length < 5) fallbackWords.push(w);
    });
  }
  var seen = {};
  fallbackWords = fallbackWords.filter(function (w) { if (seen[w]) return false; seen[w] = true; return true; });
  return fallbackWords.length >= 2 ? fallbackWords.join('-') : 'auto-distilled-skill';
}

/**
 * Convert a Gene object into SKILL.md format -- marketplace-quality content.
 *
 * @param {object} gene - Gene asset
 * @returns {string} SKILL.md content
 */
function geneToSkillMd(gene) {
  var rawName = gene.id || 'unnamed-skill';
  var name = sanitizeSkillName(rawName) || deriveFallbackName(gene);
  var displayName = toTitleCase(name);
  var desc = (gene.summary || '').replace(/[\r\n]+/g, ' ').replace(/\s*\d{10,}\s*$/g, '').trim();
  if (!desc || desc.length < 10) desc = 'AI agent skill distilled from evolution experience.';

  var lines = [
    '---',
    'name: ' + displayName,
    'description: ' + desc,
    '---',
    '',
    '# ' + displayName,
    '',
    desc,
    '',
  ];

  // -- When to Use (derived from signals; preconditions go in their own section) --
  if (gene.signals_match && gene.signals_match.length > 0) {
    lines.push('## When to Use');
    lines.push('');
    lines.push('- When your project encounters: ' + gene.signals_match.slice(0, 4).map(function (s) {
      return '`' + s + '`';
    }).join(', '));
    lines.push('');
  }

  // -- Trigger Signals --
  if (gene.signals_match && gene.signals_match.length > 0) {
    lines.push('## Trigger Signals');
    lines.push('');
    gene.signals_match.forEach(function (s) {
      lines.push('- `' + s + '`');
    });
    lines.push('');
  }

  // -- Preconditions --
  if (gene.preconditions && gene.preconditions.length > 0) {
    lines.push('## Preconditions');
    lines.push('');
    gene.preconditions.forEach(function (p) {
      lines.push('- ' + p);
    });
    lines.push('');
  }

  // -- Strategy --
  if (gene.strategy && gene.strategy.length > 0) {
    lines.push('## Strategy');
    lines.push('');
    var stepIdx = 0;
    gene.strategy.forEach(function (step) {
      var text = String(step);
      // Defensive: legacy genes may still carry "AVOID: ..." steps from
      // pre-2026-04-21 distillations. Skip them from Strategy -- the dedicated
      // "## Avoid" section below renders them correctly.
      if (/^\s*AVOID\s*[:\-]/i.test(text)) return;
      stepIdx += 1;
      var verb = extractStepVerb(text);
      if (verb) {
        lines.push(stepIdx + '. **' + verb + '** -- ' + stripLeadingVerb(text));
      } else {
        lines.push(stepIdx + '. ' + text);
      }
    });
    lines.push('');
  }

  // -- Avoid (anti-patterns, pitfalls, hard "do not" rules) --
  // Prefer the top-level `avoid` field (post-2026-04-21 genes). Fall back to
  // legacy "AVOID: ..." steps embedded in strategy so pre-existing genes still
  // surface their anti-patterns in the right section.
  var avoidItems = [];
  if (Array.isArray(gene.avoid)) {
    gene.avoid.forEach(function (a) {
      var s = String(a || '').trim();
      if (s) avoidItems.push(s);
    });
  }
  if (avoidItems.length === 0 && Array.isArray(gene.strategy)) {
    gene.strategy.forEach(function (step) {
      var text = String(step);
      var m = text.match(/^\s*AVOID\s*[:\-]\s*(.+)$/i);
      if (m) avoidItems.push(m[1].trim());
    });
  }
  if (avoidItems.length > 0) {
    lines.push('## Avoid');
    lines.push('');
    avoidItems.forEach(function (a) {
      lines.push('- ' + a);
    });
    lines.push('');
  }

  // -- Constraints --
  if (gene.constraints) {
    lines.push('## Constraints');
    lines.push('');
    if (gene.constraints.max_files) {
      lines.push('- Max files per invocation: ' + gene.constraints.max_files);
    }
    if (gene.constraints.forbidden_paths && gene.constraints.forbidden_paths.length > 0) {
      lines.push('- Forbidden paths: ' + gene.constraints.forbidden_paths.map(function (p) { return '`' + p + '`'; }).join(', '));
    }
    lines.push('');
  }

  // -- Validation --
  if (gene.validation && gene.validation.length > 0) {
    lines.push('## Validation');
    lines.push('');
    gene.validation.forEach(function (cmd) {
      lines.push('```bash');
      lines.push(cmd);
      lines.push('```');
      lines.push('');
    });
  }

  // -- Metadata --
  lines.push('## Metadata');
  lines.push('');
  lines.push('- Category: `' + (gene.category || 'innovate') + '`');
  lines.push('- Schema version: `' + (gene.schema_version || '1.6.0') + '`');
  if (gene._distilled_meta && gene._distilled_meta.source_capsule_count) {
    lines.push('- Distilled from: ' + gene._distilled_meta.source_capsule_count + ' successful capsules');
  }
  lines.push('');

  lines.push('---');
  lines.push('');
  lines.push('*This Skill was generated by [Evolver](https://github.com/EvoMap/evolver) and is distributed under the [EvoMap Skill License (ESL-1.0)](https://evomap.ai/terms). Unauthorized redistribution, bulk scraping, or republishing is prohibited. See LICENSE file for full terms.*');
  lines.push('');

  return lines.join('\n');
}

/**
 * Extract the leading verb from a strategy step for bolding.
 * Only extracts a single verb to avoid splitting compound phrases.
 * e.g. "Verify Cursor CLI installation" -> "Verify"
 *      "Run `npm test` to check" -> "Run"
 *      "Configure non-interactive mode" -> "Configure"
 *
 * Excludes anti-pattern markers ("AVOID", "DON'T", "NEVER", ...) so they never
 * get bolded as if they were real action verbs. These should be rendered as
 * anti-pattern list items in the dedicated "## Avoid" section instead.
 */
function extractStepVerb(step) {
  var ANTI_PATTERN_MARKERS = /^(AVOID|DO|DON'?T|NEVER|NOT|STOP|SKIP|IGNORE|FORBIDDEN|WARN|WARNING|CAUTION|NOTE)\b/i;
  if (ANTI_PATTERN_MARKERS.test(step)) return '';
  // Only match a capitalized verb at the very start (no leading backtick/special chars)
  var match = step.match(/^([A-Z][a-z]+)/);
  if (!match) return '';
  // Extra safety: do not treat single-capital-letter + no-lowercase abbreviations
  // (already filtered by the [a-z]+ requirement) or common non-verbs like
  // "The", "This", "These", "Those" as verbs.
  var DETERMINERS = new Set(['The', 'This', 'These', 'Those', 'That', 'A', 'An']);
  if (DETERMINERS.has(match[1])) return '';
  return match[1];
}

/**
 * Remove the leading verb from a step (already shown in bold).
 */
function stripLeadingVerb(step) {
  var verb = extractStepVerb(step);
  if (verb && step.startsWith(verb)) {
    var rest = step.slice(verb.length).replace(/^[\s:.\-]+/, '');
    return rest || step;
  }
  return step;
}

/**
 * Publish a Gene as a Skill to the Hub skill store.
 *
 * @param {object} gene - Gene asset
 * @param {object} [opts] - { category, tags }
 * @returns {Promise<{ok: boolean, result?: object, error?: string}>}
 */
function publishSkillToHub(gene, opts) {
  opts = opts || {};
  var hubUrl = getHubUrl();
  if (!hubUrl) return Promise.resolve({ ok: false, error: 'no_hub_url' });

  // Shallow-copy gene to avoid mutating the caller's object
  var geneCopy = {};
  Object.keys(gene).forEach(function (k) { geneCopy[k] = gene[k]; });
  if (Array.isArray(geneCopy.signals_match)) {
    try {
      var distiller = require('./skillDistiller');
      geneCopy.signals_match = distiller.sanitizeSignalsMatch(geneCopy.signals_match);
    } catch (e) { /* distiller not available, skip */ }
  }

  var content = geneToSkillMd(geneCopy);
  var nodeId = getNodeId();
  var fmName = content.match(/^name:\s*(.+)$/m);
  var derivedName = fmName ? fmName[1].trim().toLowerCase().replace(/[^a-z0-9]+/g, '_') : (gene.id || 'unnamed').replace(/^gene_/, '');
  // Strip ALL embedded timestamps from skillId
  derivedName = derivedName.replace(/_?\d{10,}_?/g, '_').replace(/_+/g, '_').replace(/^_|_$/g, '');
  var skillId = 'skill_' + derivedName;

  // Clean tags: use already-sanitized signals from geneCopy
  var tags = opts.tags || geneCopy.signals_match || [];
  tags = tags.filter(function (t) {
    var s = String(t || '').trim();
    return s.length >= 3 && !/^\d+$/.test(s) && !/\d{10,}/.test(s);
  });

  var body = {
    sender_id: nodeId,
    skill_id: skillId,
    content: content,
    category: opts.category || geneCopy.category || null,
    tags: tags,
  };

  var endpoint = hubUrl.replace(/\/+$/, '') + '/a2a/skill/store/publish';

  return hubFetch(endpoint, {
    method: 'POST',
    headers: buildSkillStoreHeaders(),
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(15000),
  })
    .then(function (res) { return res.json().then(function (data) { return { status: res.status, data: data }; }); })
    .then(function (result) {
      if (result.status === 201 || result.status === 200) {
        return { ok: true, result: result.data };
      }
      if (result.status === 409) {
        return updateSkillOnHub(nodeId, skillId, content, opts, gene);
      }
      return { ok: false, error: result.data?.error || 'publish_failed', status: result.status };
    })
    .catch(function (err) {
      return { ok: false, error: err.message };
    });
}

/**
 * Update an existing Skill on the Hub (new version).
 */
function updateSkillOnHub(nodeId, skillId, content, opts, gene) {
  var hubUrl = getHubUrl();
  if (!hubUrl) return Promise.resolve({ ok: false, error: 'no_hub_url' });

  var tags = opts.tags || gene.signals_match || [];
  tags = tags.filter(function (t) {
    var s = String(t || '').trim();
    return s.length >= 3 && !/^\d+$/.test(s) && !/\d{10,}/.test(s);
  });

  var body = {
    sender_id: nodeId,
    skill_id: skillId,
    content: content,
    category: opts.category || gene.category || null,
    tags: tags,
    changelog: 'Iterative evolution update',
  };

  var endpoint = hubUrl.replace(/\/+$/, '') + '/a2a/skill/store/update';

  return hubFetch(endpoint, {
    method: 'PUT',
    headers: buildSkillStoreHeaders(),
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(15000),
  })
    .then(function (res) { return res.json().then(function (data) { return { status: res.status, data: data }; }); })
    .then(function (result) {
      if (result.status >= 200 && result.status < 300) {
        return { ok: true, result: result.data };
      }
      return { ok: false, error: result.data?.error || 'update_failed', status: result.status };
    })
    .catch(function (err) { return { ok: false, error: err.message }; });
}

module.exports = {
  geneToSkillMd: geneToSkillMd,
  publishSkillToHub: publishSkillToHub,
  updateSkillOnHub: updateSkillOnHub,
  sanitizeSkillName: sanitizeSkillName,
  toTitleCase: toTitleCase,
};

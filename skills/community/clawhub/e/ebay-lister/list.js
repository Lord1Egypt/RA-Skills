#!/usr/bin/env node
/**
 * list.js — fill eBay's Create-listing form from a payload and save it as a DRAFT.
 *
 * Usage:
 *   node list.js --payload-file /tmp/ebay-payload.json [--mode draft|publish]
 *                [--draft-id <id>] [--dry-run] [--debug]
 *
 * Attaches to an already-running Chrome over CDP (default http://127.0.0.1:18800, override in
 * ebay-lister.config.json) — so it relies on that Chrome already being logged into eBay.
 *
 * Philosophy: best-effort + resilient. eBay's listing form is a dynamic React app whose
 * fields vary by category and change over time. Every field is attempted independently and
 * wrapped in try/catch; a field we can't find is recorded in `skipped[]` and the run
 * CONTINUES. At the end we always try to Save-for-later so partial work is never lost, and
 * we print a structured result the agent relays to the user.
 *
 * Output markers (grep-able by the agent / SKILL.md):
 *   DRAFT_URL=<url>           draft saved, here's where to review it
 *   DRAFT_ID=<id>             the draft this run touched — pass it back as --draft-id to RESUME
 *   PUBLISHED_URL=<url>       (only with --mode publish) listing went live
 *   DRAFT_UNAVAILABLE         could not reach a working Save-for-later control
 *   EBAY_NOT_LOGGED_IN        the Chrome isn't logged into eBay — log in and re-run
 *   FILLED=<json> SKIPPED=<json>   per-field outcome
 *
 * --draft-id resumes an EXISTING draft instead of walking the prelist again. Every prelist walk
 * creates a brand-new draft, so re-running a blocked listing used to leave a trail of duplicate
 * drafts; resume reuses the one you already have. With --mode publish and a draft id we go
 * straight to that draft's form and publish from there.
 *
 * This script does NOT decide what to list — the judgment lives in SKILL.md / the agent.
 * It will not publish unless explicitly run with --mode publish.
 */

'use strict';

const { chromium } = require('playwright-core');
const fs   = require('fs');
const path = require('path');

const SKILL_DIR = path.dirname(require.main.filename);
const LOG_FILE  = path.join(SKILL_DIR, 'runs.log');

// ── config ────────────────────────────────────────────────────────────────────
// Everything install-specific (which Chrome to attach to, your listing defaults, your category
// shortcuts, how you want to be notified) lives in ebay-lister.config.json next to this file.
// That file is gitignored; ebay-lister.config.example.json is the template. Nothing here is
// required — with no config file at all these defaults are used.
const CONFIG_FILE  = path.join(SKILL_DIR, 'ebay-lister.config.json');
const CONFIG_DEFAULTS = {
  cdpUrl: 'http://127.0.0.1:18800',
  bestOffer: 'off',                   // 'off' = force the Allow-offers toggle off; 'leave' = don't touch it
  format: {                           // defaults applied to any payload that omits them
    default: 'auction',
    startingBid: 0.99,
    durationDays: 7,
  },
  shipping: {
    service: 'USPS Ground Advantage', // preferred service class
    fillService: false,               // opt-in: also try to SET it on the form (selector unverified)
  },
  categoryIds: {},                    // keyword → eBay category id, e.g. {"video game": 139973}
  notifyCommand: null,                // optional shell command; gets the report on stdin
};
function loadConfig() {
  let user = {};
  try { user = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8')); }
  catch (e) { if (e.code !== 'ENOENT') console.error(`Ignoring bad ${path.basename(CONFIG_FILE)}: ${e.message}`); }
  const out = { ...CONFIG_DEFAULTS, ...user };
  // one level of merge is enough — every nested value is a flat scalar map
  for (const k of ['format', 'shipping', 'categoryIds']) out[k] = { ...CONFIG_DEFAULTS[k], ...(user[k] || {}) };
  return out;
}
const CONFIG  = loadConfig();
const CDP_URL = process.env.EBAY_LISTER_CDP_URL || CONFIG.cdpUrl || CONFIG_DEFAULTS.cdpUrl;

const PRELIST_URL   = 'https://www.ebay.com/sl/prelist/identify';
const SELL_FALLBACK = 'https://www.ebay.com/sl/sell';
// Review fallback. The Seller Hub drafts page (sh.ebay.com) bounces to sign-in even when the
// selling flow is authenticated, so we use the Sell hub on www.ebay.com, which stays logged in
// and lists drafts. The PRIMARY review link is the draft's own /lstng?...draftId= URL captured
// right after Save-for-later; this is only used if that URL doesn't look draft-like.
const DRAFTS_URL    = 'https://www.ebay.com/sl/sell';
// A draft's own edit URL — the review link we hand back, and the entry point for --draft-id.
const draftUrl = id => `https://www.ebay.com/lstng?mode=AddItem&draftId=${id}`;

// ── args ─────────────────────────────────────────────────────────────────────
function argVal(flag) { const i = process.argv.indexOf(flag); return i >= 0 ? process.argv[i + 1] : undefined; }
const MODE    = (argVal('--mode') || 'draft').toLowerCase();   // draft | publish
const DRY_RUN = process.argv.includes('--dry-run');
const DEBUG   = process.argv.includes('--debug');

let payload;
{
  const file = argVal('--payload-file');
  const raw  = file ? fs.readFileSync(file, 'utf8') : argVal('--json');
  if (!raw) { console.error('Provide --payload-file <path> (or --json \'<payload>\')'); process.exit(1); }
  try { payload = JSON.parse(raw); } catch (e) { console.error(`Bad payload JSON: ${e.message}`); process.exit(1); }
}

// Draft to RESUME. --draft-id wins over payload.draftId; absent = start a fresh prelist.
const RESUME_DRAFT_ID = String(argVal('--draft-id') || payload.draftId || '').replace(/\D/g, '') || null;

// ── config defaults → payload ─────────────────────────────────────────────────
// The payload only has to carry what's specific to THIS item; the rest comes from config.
function applyConfigDefaults() {
  const fmt = CONFIG.format || {};
  if (payload.format == null && fmt.default) payload.format = fmt.default;
  const auction = /auction/i.test(String(payload.format || ''));
  if (auction && payload.startingBid  == null && fmt.startingBid  != null) payload.startingBid  = fmt.startingBid;
  if (auction && payload.durationDays == null && fmt.durationDays != null) payload.durationDays = fmt.durationDays;
  if (payload.shipping && payload.shipping.service == null && CONFIG.shipping.service) {
    payload.shipping.service = CONFIG.shipping.service;
  }
  // category-id hints: longest matching keyword wins, so "video game console" beats "video game"
  if (payload.categoryId == null) {
    const hay = `${payload.categoryQuery || ''} ${payload.title || ''}`.toLowerCase();
    const hit = Object.entries(CONFIG.categoryIds || {})
      .filter(([kw]) => kw && hay.includes(String(kw).toLowerCase()))
      .sort((a, b) => b[0].length - a[0].length)[0];
    if (hit) payload.categoryId = hit[1];
  }
}
applyConfigDefaults();

const photos = (payload.photos || []).map(p => path.resolve(p));

function log(msg) {
  const line = `[${new Date().toISOString()}] ${msg}`;
  console.log(line);
  try { fs.appendFileSync(LOG_FILE, line + '\n'); } catch {}
}

// ── optional notifier hook ────────────────────────────────────────────────────
// Set "notifyCommand" in ebay-lister.config.json to any shell command and it gets the outcome
// on stdin (also as $EBAY_LISTER_MESSAGE) — pipe it to your chat bot, `mail`, ntfy, whatever.
// Default is null: this script never notifies anyone unless you ask it to.
function notify(message) {
  const cmd = CONFIG.notifyCommand;
  if (!cmd) return;
  try {
    const { spawnSync } = require('child_process');
    const res = spawnSync(cmd, {
      shell: true, input: String(message), encoding: 'utf8', timeout: 15000,
      env: { ...process.env, EBAY_LISTER_MESSAGE: String(message) },
    });
    if (res.status !== 0) log(`notifyCommand exited ${res.status}: ${(res.stderr || '').slice(0, 120)}`);
  } catch (e) { log(`notifyCommand failed: ${e.message}`); }
}

// ── payload validation (used by both dry-run and real run) ────────────────────
function validatePayload() {
  const problems = [];
  if (!payload.title) problems.push('missing "title"');
  if (payload.title && [...payload.title].length > 80) problems.push(`title is ${[...payload.title].length} chars (>80)`);
  // an auction only needs a starting bid; a fixed-price listing needs the price
  if (payload.price == null && payload.startingBid == null && MODE === 'publish') {
    problems.push('missing "price" (or "startingBid" for an auction) — required to publish');
  }
  if (!payload.condition) problems.push('missing "condition"');
  // a resumed draft already carries its photos, so they're only mandatory on a fresh listing
  if (!photos.length && !RESUME_DRAFT_ID) problems.push('no photos');
  for (const p of photos) { try { fs.accessSync(p); } catch { problems.push(`photo not found: ${p}`); } }
  return problems;
}

// ── CDP plumbing ──────────────────────────────────────────────────────────────
// Attach to a Chrome that's already running with remote debugging on CONFIG.cdpUrl. If nothing is
// listening there we try `openclaw browser start`; with any other browser setup, start your own
// Chrome with --remote-debugging-port and point cdpUrl at it.
async function ensureBrowser() {
  try {
    const r = await fetch(`${CDP_URL}/json/version`, { signal: AbortSignal.timeout(3000) });
    if (!r.ok) throw new Error('not ok');
  } catch {
    log(`CDP not reachable at ${CDP_URL} — trying \`openclaw browser start\`...`);
    const { spawnSync } = require('child_process');
    const res = spawnSync('openclaw', ['browser', 'start'], { encoding: 'utf8', timeout: 20000 });
    if (res.error || res.status !== 0) {
      throw new Error(`No Chrome on ${CDP_URL} and could not start one: ${res.error ? res.error.message : (res.stderr || res.stdout || '').trim()}`);
    }
    const deadline = Date.now() + 10000;
    while (Date.now() < deadline) {
      try {
        const r2 = await fetch(`${CDP_URL}/json/version`, { signal: AbortSignal.timeout(2000) });
        if (r2.ok) { log('Browser started, CDP ready.'); return; }
      } catch {}
      await new Promise(r => setTimeout(r, 500));
    }
    throw new Error('Browser started but CDP did not become ready in time.');
  }
}

// ── resilient field helpers ───────────────────────────────────────────────────
// Each tries a list of locator strategies in order and returns true on first success.

// Poll a condition and return the INSTANT it's true, with `max` as the ceiling. Drop-in for the
// blind `waitForTimeout(n)` sleeps this script used to be full of: identical worst case, but the
// common case returns in ~100ms instead of always paying the full sleep. (2026-07-29 — the old
// fixed sleeps added ~25s of dead time to every run.)
async function until(page, cond, max = 2000, poll = 100) {
  const deadline = Date.now() + max;
  for (;;) {
    try { if (await cond()) return true; } catch {}
    if (Date.now() >= deadline) return false;
    await page.waitForTimeout(poll);
  }
}

const count = (page, sel) => page.locator(sel).count().catch(() => 0);

async function firstVisible(page, locators, timeout = 3500) {
  for (const loc of locators) {
    try {
      const l = (typeof loc === 'function' ? loc() : loc).first();
      await l.waitFor({ state: 'visible', timeout });
      return l;
    } catch {}
  }
  return null;
}

async function tryType(page, label, value, locators) {
  if (value == null || value === '') return { label, ok: false, reason: 'no value' };
  const l = await firstVisible(page, locators);
  if (!l) return { label, ok: false, reason: 'field not found' };
  // Prefer fill() — it auto-waits for editability and dispatches React input events, and (unlike
  // click) doesn't hang waiting for the element to be un-covered. Fall back to click+type.
  try { await l.fill(String(value), { timeout: 4000 }); return { label, ok: true }; }
  catch {
    try {
      await l.click({ timeout: 3000 });
      await l.fill('').catch(() => {});
      await page.keyboard.type(String(value), { delay: 12 });
      return { label, ok: true };
    } catch (e) { return { label, ok: false, reason: ('fill ' + e.message).slice(0, 70) }; }
  }
}

// pick an option from a combobox/autocomplete: focus, type, then click the matching option
async function tryCombo(page, label, value, openLocators) {
  if (value == null || value === '') return { label, ok: false, reason: 'no value' };
  try {
    const l = await firstVisible(page, openLocators);
    if (!l) return { label, ok: false, reason: 'control not found' };
    await l.click();
    // if it's a text-ish combobox, type to filter
    await page.keyboard.type(String(value), { delay: 10 }).catch(() => {});
    // click an option whose text matches (case-insensitive, exact-ish first).
    // firstVisible already auto-waits, so the old 250ms + 500ms sleeps were pure dead time.
    const opt = await firstVisible(page, [
      () => page.getByRole('option', { name: new RegExp(`^\\s*${escapeRe(value)}\\s*$`, 'i') }),
      () => page.getByRole('option', { name: new RegExp(escapeRe(value), 'i') }),
      () => page.locator('li,[role="option"]').filter({ hasText: new RegExp(escapeRe(value), 'i') }),
    ], 2500);
    if (opt) { await opt.click(); return { label, ok: true }; }
    // no option list — maybe a free-text field that accepts Enter
    await page.keyboard.press('Enter').catch(() => {});
    return { label, ok: true, reason: 'typed (no option list matched)' };
  } catch (e) { return { label, ok: false, reason: e.message.slice(0, 80) }; }
}

function escapeRe(s) { return String(s).replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }

// eBay's custom radios: selecting a CATEGORY radio auto-navigates, so Playwright's .check()
// (which waits for the underlying input to report :checked) hangs — the page is gone before it
// flips. Use .click() for those. Condition radios stay put, so .check() is fine. Either way,
// swallow the navigation-detach race so one radio never aborts the whole run. (2026-06-19)
async function pickRadio(loc, opts = {}) {
  try {
    if (opts.click) await loc.click({ force: true, timeout: 3000 });
    else await loc.check({ force: true, timeout: 3000 });
    return true;
  } catch {
    try { await loc.click({ force: true, timeout: 2000 }); return true; } catch { return false; }
  }
}

// ── item specifics (aspects) ──────────────────────────────────────────────────
// Sanitize a value for use inside a quoted CSS attribute selector.
function cssAttr(s) { return String(s).replace(/["\\]/g, ''); }
function normLoose(s) { return String(s || '').toLowerCase().replace(/\s+/g, ' ').trim(); }

// eBay hides most aspects behind a "Show more item specifics" disclosure, and an aspect that
// isn't RENDERED can't be found by any locator — that's why free-text specifics (Model, MPN)
// silently no-op'd while the run still claimed to have filled them. Expand first, always.
// Idempotent: if the control isn't on the page we're already expanded.
async function expandItemSpecifics(page) {
  const patterns = [
    /show more item specifics/i,
    /show all item specifics/i,
    /add more (details|item specifics)/i,
    /^\s*show more\s*$/i,
  ];
  for (const re of patterns) {
    const b = page.getByRole('button', { name: re }).first();
    if (!(await b.count().catch(() => 0))) continue;
    if (!(await b.isVisible().catch(() => false))) continue;
    await b.click({ timeout: 2500 }).catch(() => {});
    await until(page, async () => !(await b.count().catch(() => 0)), 800);
  }
}

// What does this aspect's control CURRENTLY show? Returns every candidate string we can read for
// it: free-text input values plus the text of the value control in the aspect's own row. Finding
// the control by accessible NAME stops working the moment it's filled (its name becomes the
// VALUE), so we locate the row by its label text and read the control inside it.
async function aspectDisplayValues(page, name) {
  return await page.evaluate(({ aspect }) => {
    const norm = s => (s || '').replace(/\s+/g, ' ').trim();
    const target = norm(aspect).toLowerCase();
    const out = [];
    const CONTROLS = 'button, [role="button"], [role="combobox"], input, textarea';
    // 1) free-text aspects: the value lives in input.value, never in any button text
    document.querySelectorAll('input, textarea').forEach(el => {
      const names = [el.getAttribute('aria-label'), el.getAttribute('name'), el.getAttribute('placeholder')];
      if (el.id) {
        const l = document.querySelector(`label[for="${CSS.escape(el.id)}"]`);
        if (l) names.push(l.innerText);
      }
      if (names.some(n => norm(n).toLowerCase() === target) && el.value) out.push(el.value);
    });
    // 2) menu aspects: nearest ancestor of the aspect LABEL that actually holds a control
    const rows = new Set();
    document.querySelectorAll('label, span, div, dt, legend, p').forEach(el => {
      if (norm(el.innerText).toLowerCase() !== target) return;
      let p = el.parentElement;
      for (let i = 0; i < 4 && p; i++, p = p.parentElement) {
        if (p.querySelector(CONTROLS)) { rows.add(p); break; }
      }
    });
    rows.forEach(row => row.querySelectorAll(CONTROLS).forEach(c => {
      const t = c.tagName === 'INPUT' || c.tagName === 'TEXTAREA'
        ? c.value
        : norm(c.innerText) || norm(c.getAttribute('aria-label'));
      // skip the help/tooltip trigger that sits next to every aspect label
      if (t && !/^(help|info|more information|tooltip|\?|\*)$/i.test(t)) out.push(t);
    }));
    return [...new Set(out.map(norm).filter(Boolean))].slice(0, 25);
  }, { aspect: name }).catch(() => []);
}

// Is `value` what the aspect currently shows? SUBSTRING match, deliberately: the old check
// demanded a button whose accessible name EQUALED the value, which false-negatived on
// multi-selects ("Apple, Samsung"), on eBay's ellipsis truncation ("Storage Capaci…"), and on
// free-text aspects (which have no button at all). A control still showing the aspect NAME is
// empty, not filled.
async function aspectShows(page, name, value) {
  const want = normLoose(value);
  if (!want) return false;
  const shown = await aspectDisplayValues(page, name);
  return shown.some(raw => {
    const got = normLoose(raw).replace(/…|\.\.\.$/g, '').trim();
    if (!got || got === normLoose(name)) return false;
    // got contains want → multi-select ("apple, samsung" holds "apple")
    // want starts with got → eBay truncated it ("storage capaci…" for "storage capacity 64 gb")
    return got.includes(want) || (got.length >= 4 && want.startsWith(got));
  });
}

// The free-text control for an aspect, if it has one (Model, MPN, Custom Bundle …). Counted
// rather than waited on: the form is already loaded by the time we get here, and a per-locator
// wait would add seconds per aspect.
async function aspectInput(page, name) {
  const exact = new RegExp(`^\\s*${escapeRe(name)}\\s*$`, 'i');
  const attr  = cssAttr(name);
  const cands = [
    () => page.getByLabel(exact),
    () => page.locator(`input[name="${attr}" i], input[aria-label="${attr}" i]`),
    () => page.locator(`input[name*="${attr}" i], input[aria-label*="${attr}" i]`),
  ];
  for (const get of cands) {
    const l = get().first();
    if (!(await l.count().catch(() => 0))) continue;
    if (!(await l.isVisible().catch(() => false))) continue;
    if (!(await l.isEditable().catch(() => false))) continue;
    return l;
  }
  return null;
}

// Set an item-specific (aspect) the way eBay's form ACTUALLY works (cracked 2026-06-19, after the
// old role=option approach silently failed and blocked publish on required specifics like Platform):
//   0. EXPAND the collapsed specifics section, then bail early if the aspect already shows the
//      value — see the toggle trap below.
//   1. FREE-TEXT aspects (Model, MPN) are plain inputs, not menu buttons. getByRole('button',
//      {name:/^Model$/}) never matched them, so they were skipped in silence; fill() them.
//   2. click the aspect's value button (LAST match — the FIRST is just a help-tooltip trigger)
//   3. type the value into its search box: input[name="search-box-attributes<Aspect>"] — REAL
//      keystrokes, which is what triggers the filter menu (fill() alone doesn't)
//   4. click the matching result. eBay ships (at least) TWO skins of this widget and the option
//      element differs between them:
//        a) div[role="menuitemcheckbox"].filter-menu__item
//        b) .se-filter-menu-button__list-menu[role="menu"] > … (no menuitemcheckbox role at all)
//      Only (a) was handled, so on category 31510 (Laptop Power Adapters/Chargers) the Brand
//      aspect found no option, fell through to Enter, and setAspect returned TRUE anyway — the run
//      reported "specific:Brand" filled while eBay kept rejecting "The item specific Brand is
//      missing". (2026-07-29)
//   5. VERIFY the value actually stuck, by READING the control (aspectShows), not by demanding a
//      button whose name equals the value.
// TOGGLE TRAP: a menuitemcheckbox is a TOGGLE. resolveRequired() re-runs setAspect on retry, and
// re-clicking an already-selected option UNCHECKS it — the retry loop used to un-fill the very
// specific it had just filled. Hence the early return, plus the aria-checked guard at the click.
async function setAspect(page, name, value) {
  await expandItemSpecifics(page);
  if (await aspectShows(page, name, value)) return true;   // already set — touching it would clear it

  // free-text aspect: no menu, just an input
  const textInput = await aspectInput(page, name);
  if (textInput) {
    try {
      await textInput.fill(String(value), { timeout: 3000 });
      await textInput.press('Tab').catch(() => {});   // commit + dismiss any suggestion list
      if (await aspectShows(page, name, value)) return true;
    } catch {}
  }

  const btn = page.getByRole('button', { name: new RegExp(`^${escapeRe(name)}$`, 'i') }).last();
  if (!(await btn.count().catch(() => 0))) return false;
  await btn.click({ timeout: 3500 }).catch(() => {});
  const inp = page.locator(`input[name="search-box-attributes${cssAttr(name)}"]`).first();
  await until(page, async () => await inp.count().catch(() => 0) > 0, 800);
  if (await inp.count().catch(() => 0)) await inp.click().catch(() => {});
  await page.keyboard.type(String(value), { delay: 15 }); // real keystrokes trigger the filter menu
  const re = new RegExp(escapeRe(value), 'i');
  // every known skin of the option list, most specific first
  // Scope EVERY option lookup to the aspect menu that's currently open. Searching the whole page
  // for `.menu__item` also matches eBay's header navigation, and clicking one of those silently
  // dismissed the aspect popover — which knocked out every specific in the run, not just this one.
  const menu = page.locator('[role="menu"]:visible').last();
  const optionSets = [
    // MULTI-select aspects render menuitemcheckbox; SINGLE-select ones render menuitemradio.
    // Only the checkbox role was handled, which is why Brand on category 31510 never took.
    () => menu.getByRole('menuitemradio', { name: re }).first(),
    () => menu.getByRole('menuitemcheckbox', { name: re }).first(),
    () => menu.locator('.menu__item, .filter-menu__item').filter({ hasText: re }).first(),
    () => menu.locator('[role="menuitem"], li').filter({ hasText: re }).first(),
  ];
  const anyOption = async () => {
    for (const get of optionSets) { const l = get(); if (await l.count().catch(() => 0)) return l; }
    return null;
  };
  await until(page, async () => !!(await anyOption()), 1500);
  const opt = await anyOption();
  if (opt) {
    // aria-checked="true" means this option is ALREADY selected. Clicking it would toggle the
    // value back off (menuitemcheckbox is a toggle), so leave it alone and go verify instead.
    const checked = await opt.getAttribute('aria-checked').catch(() => null);
    if (checked !== 'true') await opt.click().catch(() => {}); // constrained aspect: pick the real option
  } else {
    // no match — some aspects allow a free-text "Add custom value" entry; use it, else plain Enter
    const custom = menu.getByText(/add custom value/i).first();
    if (await custom.count().catch(() => 0)) await custom.click().catch(() => {});
    else await page.keyboard.press('Enter').catch(() => {});
  }
  const apply = page.getByRole('button', { name: /^(apply|done|save)$/i }).first();
  if (await apply.count().catch(() => 0)) await apply.click().catch(() => {});
  else await page.keyboard.press('Escape').catch(() => {});
  await until(page, async () => !(await count(page, '.filter-menu__item')), 700);
  // Verify by READING the control (value button text, or input.value for free-text), accepting a
  // substring. The old check — "a button exists whose accessible name equals the value" — reported
  // failure for values that were perfectly well set but rendered joined, truncated, or in an input.
  return await until(page, () => aspectShows(page, name, value), 1500);
}

async function clickByText(page, names, timeout = 4000) {
  for (const name of names) {
    const l = await firstVisible(page, [
      () => page.getByRole('button', { name: new RegExp(escapeRe(name), 'i') }),
      () => page.getByRole('link',   { name: new RegExp(escapeRe(name), 'i') }),
      () => page.locator('button, a, [role="button"]').filter({ hasText: new RegExp(escapeRe(name), 'i') }),
    ], timeout);
    if (l) { try { await l.click(); return name; } catch {} }
  }
  return null;
}

// How many photos does the form already show? Read eBay's own "N/25" counter — counting <img>
// elements catches thumbnails, icons and previews and lies. 0 when there's no counter.
async function photoCount(page) {
  return await page.evaluate(() => {
    const m = (document.body.innerText || '').match(/\b(\d{1,2})\s*\/\s*25\b/);
    return m ? Number(m[1]) : 0;
  }).catch(() => 0);
}

async function snap(page, tag) {
  if (!DEBUG) return;
  try { await page.screenshot({ path: path.join(SKILL_DIR, `debug-${tag}.png`), fullPage: false }); } catch {}
}

// eBay uses TWO condition schemes depending on category:
//   • standard:  New=1000, New other/Open box=1500, Used=3000, For parts=7000
//   • graded (video games, trading cards, …): Brand New=1000, Like New=2750,
//     Very Good=4000, Good=5000, Acceptable=6000  (there is NO 3000 here)
// Map the payload's free-text condition to candidates covering BOTH, tried value-first then
// by visible label, so one payload works across categories. (Cracked 2026-06-19: video games
// silently failed for weeks because the script only knew value 3000, which doesn't exist there.)
function conditionCandidates(cond) {
  const c = String(cond || 'used').toLowerCase().trim();
  const T = {
    'new':                      { values: ['1000'],                 labels: [/^\s*new\s*$/i, /brand new/i] },
    'brand new':                { values: ['1000'],                 labels: [/brand new/i, /^\s*new\s*$/i] },
    'new other':                { values: ['1500', '2750'],         labels: [/new other/i, /open box/i, /like new/i] },
    'open box':                 { values: ['1500', '2750'],         labels: [/open box/i, /like new/i, /new other/i] },
    'like new':                 { values: ['2750', '1500'],         labels: [/like new/i, /open box/i] },
    'used':                     { values: ['3000', '4000'],         labels: [/^\s*used\s*$/i, /very good/i] },
    'very good':                { values: ['4000', '3000'],         labels: [/very good/i, /^\s*used\s*$/i] },
    'excellent':                { values: ['4000', '2750', '3000'], labels: [/very good/i, /like new/i] },
    'good':                     { values: ['5000', '3000'],         labels: [/^\s*good\s*$/i, /^\s*used\s*$/i] },
    'acceptable':               { values: ['6000', '7000', '3000'], labels: [/acceptable/i, /^\s*used\s*$/i] },
    'for parts or not working': { values: ['7000', '6000'],         labels: [/for parts/i, /not working/i, /acceptable/i] },
  };
  return T[c] || { values: ['3000', '4000'], labels: [/^\s*used\s*$/i, /very good/i] };
}

// ── stuck handoff ──────────────────────────────────────────────────────────────
// Bail FAST instead of grinding through timeouts on the wrong page. Emit a structured
// report (URL + screenshot + the choices on screen) so the agent can decide the one step
// and re-run with the answer (e.g. payload.categoryId). This is the "doesn't hang forever
// + agent figures out how to proceed" behavior.
async function stuckReport(page, step) {
  const url = page.url();
  const shot = path.join(SKILL_DIR, 'debug-stuck.png');
  try { await page.screenshot({ path: shot }); } catch {}
  const cats = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll('input[type="radio"][name="categoryId"]').forEach(r => {
      let t = ''; const id = r.id;
      if (id) { const l = document.querySelector(`label[for="${id}"]`); if (l) t = l.innerText; }
      if (!t) { const p = r.closest('label,li,div'); if (p) t = p.innerText; }
      out.push({ value: r.value || '', label: (t || '').replace(/\s+/g, ' ').trim().slice(0, 90) });
    });
    return out;
  }).catch(() => []);
  const buttons = await page.$$eval('button,a[role="button"],[role="button"]',
    els => [...new Set(els.filter(e => e.offsetParent !== null)
      .map(e => (e.innerText || e.getAttribute('aria-label') || '').replace(/\s+/g, ' ').trim())
      .filter(Boolean))].slice(0, 20)).catch(() => []);
  const conds = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll('input[type="radio"][name="condition"]').forEach(r => {
      let t = ''; const id = r.id;
      if (id) { const l = document.querySelector(`label[for="${id}"]`); if (l) t = l.innerText; }
      if (!t) { const p = r.closest('label,li,div'); if (p) t = p.innerText; }
      out.push({ value: r.value || '', label: (t || '').replace(/\s+/g, ' ').trim().slice(0, 60) });
    });
    return out;
  }).catch(() => []);
  // Be honest about WHERE we're stuck. The condition node masquerades under a category-looking
  // URL (view=sellnode-condition) — don't report "category" when there are no category radios.
  let realStep = step;
  if (/view=sellnode-condition/.test(url)) realStep = conds.length ? 'condition-select' : 'product-match';
  console.log(`STUCK_AT=${realStep}`);
  console.log(`STUCK_URL=${url}`);
  console.log(`STUCK_SCREENSHOT=${shot}`);
  console.log(`STUCK_CATEGORIES=${JSON.stringify(cats)}`);
  console.log(`STUCK_CONDITIONS=${JSON.stringify(conds)}`);
  console.log(`STUCK_BUTTONS=${JSON.stringify(buttons)}`);
  log(`STUCK_AT=${realStep} url=${url} categories=${cats.length} conditions=${conds.length}`);
}

// ── publish-time validation recovery ─────────────────────────────────────────────
// Scrape eBay's on-form validation messages that appear when "List it" is blocked by a
// missing required field. Best-effort across eBay's shifting class names.
// eBay renders its success banner ("Your listing is now live") into an [aria-live] region — the
// SAME place collectErrors() scrapes — so a successful publish used to land in the ERROR list and
// get reported as blocked. That's how the 2026-06-29 run published and then still fell back
// to "draft save" (runs.log). Success is therefore: the /success redirect OR that banner.
const LIVE_BANNER = /your listing is now live|listing is live|congratulations.{0,40}listed/i;

async function publishSucceeded(page) {
  if (/\/success|[?&]itemid=/i.test(page.url())) return true;
  return await page.evaluate(re => new RegExp(re, 'i').test(document.body.innerText || ''),
    LIVE_BANNER.source).catch(() => false);
}

// A REAL validation message, not just any text living inside an [aria-live]/[class*=error] box.
// The old sweep returned the title character counter ("0/800") and the price field's "Starting
// bid $" adornment as "errors", so resolveRequired() chased phantoms and the publish loop burned
// its 3 retries on nothing. Two gates now: eBay's exact item-specific miss, or a sentence that
// actually states a problem.
const ASPECT_MISSING = /the item specific\s+(.+?)\s+is missing/i;
const REAL_ERROR = /(is missing|is required|are required|please (add|select|enter|choose|provide|fix)|must (be|have|contain|include)|cannot be|can't be|enter a valid|needs? to be|before you can|to continue|fix the following)/i;
// counters ("0/800"), lone currency/unit adornments, bare numbers — never errors
const NOT_AN_ERROR = /^\s*(\d+\s*\/\s*\d+|[$€£]|\d+(\.\d+)?\s*(lb|lbs|oz|in|g|kg)?)\s*$/i;

// Item-specific names eBay explicitly flagged, e.g. "The item specific Brand is missing" → Brand.
function missingAspectNames(errors) {
  const out = [];
  for (const e of errors) {
    const m = String(e).match(ASPECT_MISSING);
    if (m && m[1]) out.push(m[1].replace(/[.:]$/, '').trim());
  }
  return [...new Set(out)];
}

async function collectErrors(page) {
  return await page.evaluate(() => {
    const seen = new Set(), out = [];
    const add = t => { t = (t || '').replace(/\s+/g, ' ').trim(); if (t && t.length < 160 && !seen.has(t)) { seen.add(t); out.push(t); } };
    document.querySelectorAll('[role="alert"], [class*="error" i], [class*="inline-notice" i], [aria-live]').forEach(e => { if (e.offsetParent !== null) add(e.innerText); });
    document.querySelectorAll('span,div,p,label').forEach(e => {
      const t = e.innerText || '';
      if (/required|please (add|select|enter)|is missing|must (be|have)|to continue/i.test(t) && t.length < 120 && e.offsetParent !== null) add(t);
    });
    return out.slice(0, 40);
  }).then(list => list
    .filter(t => !LIVE_BANNER.test(t))
    .filter(t => !NOT_AN_ERROR.test(t))
    .filter(t => ASPECT_MISSING.test(t) || REAL_ERROR.test(t))
    .slice(0, 25)
  ).catch(() => []);
}

// Given the validation messages, fill the required fields we can FROM THE PAYLOAD, then signal a
// retry. Deliberately does NOT fabricate values — if a flagged field has no payload data we can't
// safely satisfy it, so we return false and let the caller fall back to saving a draft + reporting.
async function resolveRequired(page, errors, payload, record) {
  const blob = errors.join(' | ').toLowerCase();
  let fixed = false;
  if (/price|buy it now|starting bid/.test(blob) && payload.price != null) {
    const r = await tryType(page, 'price (recover)', payload.price, [
      () => page.getByRole('textbox', { name: /buy it now/i }),
      () => page.getByLabel(/buy it now price|^price$/i),
      () => page.locator('input[aria-label*="price" i]'),
    ]);
    if (r.ok) { record(r); fixed = true; }
  }
  if (/condition/.test(blob)) {
    const _cs = [];
    if (payload.conditionGrade) _cs.push(conditionCandidates(payload.conditionGrade));
    _cs.push(conditionCandidates(payload.condition));
    for (const v of [...new Set(_cs.flatMap(c => c.values))]) {
      const r = page.locator(`input[type="radio"][name="condition"][value="${v}"]`);
      if (await r.count().catch(() => 0)) { if (await pickRadio(r)) { record({ label: 'condition (recover)', ok: true }); fixed = true; } break; }
    }
  }
  // Only item specifics eBay actually flagged AND we have a value for. Prefer the aspect names
  // parsed out of "The item specific <X> is missing" — a bare substring match against the whole
  // error blob retried aspects that were never flagged, and setAspect on an already-set
  // multi-select TOGGLES IT OFF.
  const flagged = missingAspectNames(errors).map(n => n.toLowerCase());
  for (const [k, val] of Object.entries(payload.itemSpecifics || {})) {
    if (val == null || val === '') continue;
    const key = k.toLowerCase();
    const wanted = flagged.length
      ? flagged.some(f => f === key || f.includes(key) || key.includes(f))
      : blob.includes(key);
    if (!wanted) continue;
    try { if (await setAspect(page, k, val)) { record({ label: `specific:${k} (recover)`, ok: true }); fixed = true; } } catch {}
  }
  return fixed;
}

// ── the listing flow ──────────────────────────────────────────────────────────
async function run() {
  await ensureBrowser();
  const browser = await chromium.connectOverCDP(CDP_URL);
  const ctx  = browser.contexts()[0] ?? await browser.newContext();
  const page = await ctx.newPage();
  // Cap EVERY action at 5s — be aggressive, 5s is always enough for this form to load. Playwright's
  // default is 30s, which turned a few unactionable fields into a 5-minute grind. Fail fast.
  page.setDefaultTimeout(5000);
  page.setDefaultNavigationTimeout(45000);
  const filled = [], skipped = [];
  const record = (r) => { (r.ok ? filled : skipped).push(r.reason ? `${r.label} (${r.reason})` : r.label); };

  try {
    // 1) login check — resuming goes STRAIGHT to the existing draft's form; otherwise start at the
    //    prelist. Every prelist walk mints a NEW draft, which is why re-running a blocked listing
    //    used to litter the account with duplicates. --draft-id reuses the one you already have.
    const startUrl = RESUME_DRAFT_ID ? draftUrl(RESUME_DRAFT_ID) : PRELIST_URL;
    log(RESUME_DRAFT_ID ? `Resuming draft ${RESUME_DRAFT_ID} (${startUrl})` : `Navigating to prelist (${startUrl})`);
    await page.goto(startUrl, { waitUntil: 'domcontentloaded', timeout: 45000 });
    // settle only until we can tell which page we landed on: signin redirect, the category box,
    // or (resume) the listing form itself
    await until(page, async () =>
      /signin\.ebay\.com|\/signin/.test(page.url()) || /\/lstng/.test(page.url())
      || await count(page, 'input[type="text"],[role="combobox"]'), 1500);
    if (/signin\.ebay\.com|\/signin/.test(page.url())) {
      console.log('EBAY_NOT_LOGGED_IN');
      log('EBAY_NOT_LOGGED_IN — Chrome is not logged into eBay.');
      return;
    }
    await snap(page, '1-prelist');

    // On a resume we're already on the form — the whole prelist below is skipped.
    let reachedForm = /\/lstng/.test(page.url());
    if (RESUME_DRAFT_ID && !reachedForm) {
      // the draft id is wrong/expired/belongs to another account — say so instead of silently
      // starting a fresh prelist and creating yet another duplicate draft
      await stuckReport(page, 'draft-resume');
      return;
    }

    // 2) CATEGORY — type the query into the category combobox; eBay shows category radios.
    //    (Learned 2026-06-18: this is the step that used to hang. See README "real eBay flow".)
    const q = payload.categoryQuery || payload.title;
    const qBox = reachedForm ? null : await firstVisible(page, [
      () => page.getByRole('combobox'),
      () => page.getByPlaceholder(/enter a category value|what.*selling|search/i),
      () => page.locator('input[aria-label="Enter a category value"]'),
      () => page.locator('input[type="text"]'),
    ], 6000);
    if (qBox) {
      await qBox.click();
      await page.keyboard.type(String(q), { delay: 8 });
      // let the category radios populate — proceed as soon as they exist, or the page moved on
      await until(page, async () =>
        /\/lstng/.test(page.url())
        || await count(page, 'input[type="radio"][name="categoryId"],input[type="radio"][name="condition"]'), 2500);
      record({ label: 'category query', ok: true });
    } else if (!reachedForm) {
      record({ label: 'category query', ok: false, reason: 'category box not found' });
    }
    await snap(page, '2-identify');

    // PRELIST NAVIGATION — eBay's prelist is a VARIABLE multi-step flow whose order changes per
    // item: category-picker (radios name=categoryId + "Done") → product-match ("Find a match"
    // list) → condition node (radios name=condition) → listing form (/lstng). Hard-coding one
    // order with a single end-guard stranded video games for weeks (cracked 2026-06-19). Instead
    // LOOP: detect whichever sub-view we're on, take the one sensible action, repeat until /lstng.
    // (No-op on a resume — reachedForm is already true.)
    for (let hop = 0; hop < 8 && !reachedForm; hop++) {
      if (/\/lstng/.test(page.url())) { reachedForm = true; break; }
      const hasCategory  = await page.locator('input[type="radio"][name="categoryId"]').count().catch(() => 0);
      const hasCondition = await page.locator('input[type="radio"][name="condition"]').count().catch(() => 0);

      if (hasCondition) {
        // condition sub-view — prefer finer conditionGrade ("Like New"), else condition; select by
        // value across BOTH schemes (standard Used=3000 vs graded 2750/4000/5000/6000), then label.
        const _cs = [];
        if (payload.conditionGrade) _cs.push(conditionCandidates(payload.conditionGrade));
        _cs.push(conditionCandidates(payload.condition));
        const cand = { values: [...new Set(_cs.flatMap(c => c.values))], labels: _cs.flatMap(c => c.labels) };
        let set = false;
        for (const v of cand.values) {
          const r = page.locator(`input[type="radio"][name="condition"][value="${v}"]`);
          if (await r.count().catch(() => 0)) { set = await pickRadio(r); if (set) { record({ label: `condition=${payload.conditionGrade || payload.condition} (value ${v})`, ok: true }); break; } }
        }
        if (!set) for (const re of cand.labels) {
          const r = page.getByRole('radio', { name: re }).first();
          if (await r.count().catch(() => 0)) { set = await pickRadio(r); if (set) { record({ label: `condition (label ${re.source})`, ok: true }); break; } }
        }
        if (!set) record({ label: `condition=${payload.condition}`, ok: false, reason: 'no matching condition radio' });
        await clickByText(page, ['Continue to listing', 'Continue', 'Done'], 5000);
        // advance as soon as this sub-view is actually gone, rather than always sleeping 2s
        await until(page, async () =>
          /\/lstng/.test(page.url()) || !(await count(page, 'input[type="radio"][name="condition"]')), 2500);
        continue;
      }

      if (hasCategory) {
        // category-picker — choose payload.categoryId if given, else the FIRST radio (eBay sorts
        // best-match first, e.g. 139973 Video Games), then click "Done"/Continue.
        let picked = false, pickedVal = payload.categoryId;
        if (payload.categoryId) {
          const r = page.locator(`input[type="radio"][name="categoryId"][value="${payload.categoryId}"]`);
          if (await r.count().catch(() => 0)) picked = await pickRadio(r, { click: true });
        }
        if (!picked) {
          const first = page.locator('input[type="radio"][name="categoryId"]').first();
          if (await first.count().catch(() => 0)) { pickedVal = await first.getAttribute('value').catch(() => null); picked = await pickRadio(first, { click: true }); }
        }
        record({ label: `categoryId=${pickedVal || '?'}${payload.categoryId ? '' : ' (best-match)'}`, ok: picked });
        // selecting the radio often auto-advances; if a Done/Continue control remains, click it.
        await clickByText(page, ['Done', 'Continue to listing', 'Continue'], 4000);
        await until(page, async () =>
          /\/lstng/.test(page.url()) || !(await count(page, 'input[type="radio"][name="categoryId"]')), 2500);
        continue;
      }

      // neither set of radios — likely a product-match list; dismiss it and re-loop
      const advanced = async () => until(page, async () =>
        /\/lstng/.test(page.url())
        || await count(page, 'input[type="radio"][name="categoryId"],input[type="radio"][name="condition"]'), 2500);
      if (await clickByText(page, ['Continue without match', 'Continue without', 'No match'], 3000)) { await advanced(); continue; }
      // nothing actionable — try a generic forward control, else stop looping
      if (!(await clickByText(page, ['Continue to listing', 'Continue', 'Next'], 3000))) break;
      await advanced();
    }
    await snap(page, '3-prelist-done');

    // 4) GUARD — we MUST be on the listing form now. If not, BAIL FAST with a stuck report
    //    instead of grinding through form-field timeouts on the wrong page (the old 3-min spin-out).
    const onForm = reachedForm || await page.waitForURL(/\/lstng/, { timeout: 6000 }).then(() => true).catch(() => false);
    if (!onForm) { await stuckReport(page, 'prelist'); return; }
    // Readiness gate: wait for the title input to actually render before filling, so we don't race
    // the form load. If it never appears, bail with a report rather than grinding every field.
    const titleReady = await page.locator('input[name="title"]').first()
      .waitFor({ state: 'visible', timeout: 10000 }).then(() => true).catch(() => false);
    if (!titleReady) { await stuckReport(page, 'form-not-ready'); return; }
    const draftId = (page.url().match(/draftId=(\d+)/) || [])[1] || RESUME_DRAFT_ID || null;
    if (draftId) { log(`form reached, draftId=${draftId}`); console.log(`DRAFT_ID=${draftId}`); }

    // 4) PHOTOS — upload all via the hidden file input. A RESUMED draft already has its photos, and
    //    setInputFiles appends rather than replaces, so uploading again just duplicates them.
    const existingPhotos = RESUME_DRAFT_ID ? await photoCount(page) : 0;
    if (photos.length && existingPhotos > 0) {
      record({ label: `photos (${existingPhotos} already on draft)`, ok: true, reason: 'resume — not re-uploaded' });
    } else if (photos.length) {
      try {
        const fileInput = page.locator('input[type="file"]').first();
        await fileInput.waitFor({ state: 'attached', timeout: 8000 });
        // Long timeout: many photos take >5s to attach. With the 5s page default this threw a
        // FALSE timeout even though the upload SUCCEEDED — which led to a misleading re-upload and
        // duplicate photos. Always give setInputFiles room, and verify the N/25 count before any retry.
        await fileInput.setInputFiles(photos, { timeout: 90000 }); // upload ONCE — re-uploading duplicates
        // wait for thumbnails / upload to settle — stop as soon as eBay's own "N/25" counter shows
        // every photo landed; keep the old duration only as the ceiling.
        const nOf25 = new RegExp(`\\b${photos.length}\\s*/\\s*25\\b`);
        await until(page,
          async () => await page.getByText(nOf25).count().catch(() => 0) > 0,
          Math.min(3000 + photos.length * 1500, 12000), 250);
        record({ label: `photos (${photos.length})`, ok: true });
      } catch (e) { record({ label: 'photos', ok: false, reason: e.message.slice(0, 80) }); }
    }
    await snap(page, '4-photos');

    // 5) TITLE — input[name="title"] is the proven selector (try it first).
    record(await tryType(page, 'title', payload.title, [
      () => page.locator('input[name="title"]'),
      () => page.locator('input[name*="title" i]'),
      () => page.getByPlaceholder(/title/i),
      () => page.locator('input[aria-label*="title" i]'),
    ]));

    // 6) CONDITION — already set in the prelist condition node (carries onto the form). We do NOT
    //    re-select it here: opening the on-form condition dropdown left an overlay that made every
    //    field below it unclickable (the 5-min grind). If a grade is needed, the agent sets it in
    //    review. (Intentionally no-op.)

    // 7) ITEM SPECIFICS — fill only the ones we were given, via setAspect() (the real
    //    menuitemcheckbox picker). Required specifics we can't match here are caught at publish by
    //    resolveRequired(). We intentionally do NOT try to populate every possible aspect.
    for (const [k, v] of Object.entries(payload.itemSpecifics || {})) {
      if (v == null || v === '') { skipped.push(`specific:${k} (no value)`); continue; }
      try {
        const ok = await setAspect(page, k, v);
        if (ok) record({ label: `specific:${k}`, ok: true });
        else skipped.push(`specific:${k} (no matching option)`);
      } catch (e) { skipped.push(`specific:${k} (${e.message.slice(0, 35)})`); }
    }

    // 8) DESCRIPTION — it's a rich-text editor in an iframe titled "Description" (frame
    //    se-rte-frame__summary). NOT the first <textarea> — that one is "itemConditionDescription"
    //    (the condition box). Click the iframe body and type. (Verified 2026-06-19.)
    if (payload.description) {
      // When Best Offer is force-disabled (config bestOffer:"off", step 10b), scrub any "offers
      // welcome / or best offer" language — a live listing that invites offers it won't accept is
      // worse than silence. With bestOffer:"leave" the copy is left exactly as written.
      const desc = String(CONFIG.bestOffer || 'off').toLowerCase() !== 'off'
        ? String(payload.description)
        : String(payload.description)
          .replace(/\s*\boffers?\s+(are\s+)?(welcome|considered|accepted|encouraged|ok|invited)\b[.!]?/gi, '')
          .replace(/\s*\b(or\s+)?best\s+offers?\b[.!]?/gi, '')
          .replace(/[ \t]{2,}/g, ' ').replace(/\n{3,}/g, '\n\n').trim();
      let ok = false;
      try {
        const body = page.frameLocator('iframe[title="Description" i], iframe[aria-label="Description" i]').locator('body').first();
        await body.click({ timeout: 4000 });
        await page.keyboard.type(desc, { delay: 3 });
        ok = true;
      } catch {}
      if (ok) record({ label: 'description', ok: true });
      else record(await tryType(page, 'description', desc, [
        () => page.locator('textarea[aria-label="Description" i]'),
        () => page.getByLabel(/^description$/i),
      ]));
    }

    // 9) FORMAT — "Buy It Now" and "Auction" are buttons/tabs on the form (NOT a combobox). Click
    //    the one the payload asks for. For auction we then set a starting bid (9b) + optional BIN (10).
    const wantAuction = payload.format && /auction/i.test(payload.format);
    if (payload.format) {
      try {
        const want = wantAuction ? /^auction$/i : /^buy it now$/i;
        let done = false;
        const btn = page.getByRole('button', { name: want }).first();
        if (await btn.count().catch(() => 0)) { await btn.click().catch(() => {}); done = true; }
        if (!done && !wantAuction) {
          const fmtBtn = page.getByRole('button', { name: /^format$/i }).first();
          if (await fmtBtn.count().catch(() => 0)) {
            await fmtBtn.click({ timeout: 3000 }); await page.waitForTimeout(500);
            const opt = page.getByRole('option', { name: /buy it now|fixed price/i }).first();
            if (await opt.count().catch(() => 0)) { await opt.click(); done = true; }
            else await page.keyboard.press('Escape');
          }
        }
        record({ label: `format:${wantAuction ? 'auction' : 'fixed'}`, ok: done, reason: done ? undefined : 'control not found' });
        await page.waitForTimeout(1000);
      } catch (e) { record({ label: 'format', ok: false, reason: e.message.slice(0, 40) }); }
    }

    // 9b) STARTING BID (auction) — eBay requires it for auction format.
    if (wantAuction && payload.startingBid != null) {
      record(await tryType(page, 'starting bid', payload.startingBid, [
        () => page.getByRole('textbox', { name: /starting bid|start price/i }),
        () => page.getByLabel(/starting bid|start price/i),
        () => page.locator('input[name*="startPrice" i], input[aria-label*="starting" i]'),
      ]));
    }

    // 9c) AUCTION DURATION — eBay defaults auctions to 7 days; set it explicitly when the payload
    //     asks (e.g. 5 days to make this end alongside another listing). The Duration control only
    //     appears for auction format; its options read "1 day"/"3 days"/"5 days"/"7 days"/"10 days".
    if (wantAuction && payload.durationDays != null) {
      const durLabel = `${payload.durationDays} day${Number(payload.durationDays) === 1 ? '' : 's'}`;
      record(await tryCombo(page, 'duration', durLabel, [
        () => page.getByRole('combobox', { name: /duration/i }),
        () => page.getByLabel(/duration/i),
        () => page.getByRole('button', { name: /duration/i }),
        () => page.getByRole('button', { name: /^\d+\s*days?$/i }),
      ]));
    }

    // 10) PRICE — fixed: the item price; auction: the OPTIONAL Buy It Now price (eBay requires it be
    //     ≥30% above the starting bid). input[name="price"] (aria "Item price") is the proven selector.
    if (payload.price != null) {
      record(await tryType(page, wantAuction ? 'buy it now price' : 'price', payload.price, [
        () => page.locator('input[name="price"]'),
        () => page.getByRole('textbox', { name: /buy it now/i }),
        () => page.getByLabel(/buy it now price|^price$|^item price$/i),
        () => page.locator('input[aria-label*="price" i], input[name*="price" i]'),
      ]));
    }

    // 10b) BEST OFFER — config "bestOffer": "off" (default) forces the "Allow offers" toggle OFF, so
    //      you never receive buyer offers; "leave" means don't touch whatever eBay defaults to. eBay
    //      sometimes pre-enables it. If the control isn't present for the category/format, that's
    //      fine — recorded as skipped, never fatal.
    if (String(CONFIG.bestOffer || 'off').toLowerCase() !== 'off') {
      record({ label: 'bestOffer', ok: true, reason: 'left at eBay default per config' });
    } else try {
      const findToggle = () => {
        for (const role of ['switch', 'checkbox']) {
          const el = page.getByRole(role, { name: /allow offers|best offer|accept offers/i }).first();
          if (el) return el;
        }
        return null;
      };
      const toggle = findToggle();
      const present = toggle && (await toggle.count().catch(() => 0));
      if (present && (await toggle.isChecked().catch(() => false))) {
        await toggle.click({ timeout: 3000 });
        record({ label: 'bestOffer:off', ok: true });
      } else if (present) {
        record({ label: 'bestOffer:off', ok: true, reason: 'already off' });
      } else {
        record({ label: 'bestOffer:off', ok: false, reason: 'toggle not found' });
      }
    } catch (e) { record({ label: 'bestOffer:off', ok: false, reason: e.message.slice(0, 40) }); }

    // 11) SHIPPING weight + dimensions. eBay needs WHOLE pounds + ounces separately — a fractional
    //     "0.1 lb" silently fails to save (that was the "Package size" validation error). For light
    //     items set weightLb:0 and weightOz:N.
    if (payload.shipping) {
      const s = payload.shipping;
      const map = [
        ['weight (lb)', s.weightLb, [/enter weight in pounds/i, /weight.*pound/i]],
        ['weight (oz)', s.weightOz, [/enter weight in ounces/i, /weight.*ounce/i]],
        // Anchor on eBay's exact package-dimension labels FIRST. The loose /depth|height/ pattern
        // matched the "Item Height" ITEM SPECIFIC instead of the shipping box depth, so the depth
        // field silently stayed empty while the run still reported "height (in)" filled. (2026-07-29)
        ['length (in)', s.lengthIn, [/enter package length in inches/i, /package length/i, /length/i]],
        ['width (in)',  s.widthIn,  [/enter package width in inches/i, /package width/i, /width/i]],
        ['height (in)', s.heightIn, [/enter package depth in inches/i, /enter package height in inches/i, /package (depth|height)/i]],
      ];
      for (const [label, val, res] of map) {
        if (val == null) continue;
        record(await tryType(page, label, val, res.map(re => () => page.getByLabel(re))));
      }
      // SHIPPING SERVICE — opt-in (config shipping.fillService). eBay's service picker varies a lot
      // by category and account, and a half-opened dropdown leaves an overlay that can swallow the
      // "List it" click, so the default is to leave whatever service the account is set up with.
      if (CONFIG.shipping.fillService && s.service) {
        record(await tryCombo(page, 'shipping service', s.service, [
          () => page.getByRole('combobox', { name: /shipping service|service/i }),
          () => page.getByLabel(/shipping service/i),
          () => page.getByRole('button', { name: /shipping service/i }),
        ]));
        await page.keyboard.press('Escape').catch(() => {});   // make sure nothing stays open
      }
    }
    await snap(page, '5-filled');

    log(`FILLED=${JSON.stringify(filled)}`);
    log(`SKIPPED=${JSON.stringify(skipped)}`);
    console.log(`FILLED=${JSON.stringify(filled)}`);
    console.log(`SKIPPED=${JSON.stringify(skipped)}`);

    // 12) PUBLISH (with required-field recovery) or SAVE DRAFT.
    //   eBay validates on "List it": on success it redirects to /sl/success?...itemid=NNN; if a
    //   required field is missing it stays on the form and shows inline errors. So we LOOP: click
    //   List it → if published, done → else read the errors, fill what we can from the payload, and
    //   retry. If we still can't satisfy it, fall through and save a DRAFT so nothing is lost.
    if (MODE === 'publish') {
      let publishedUrl = null;
      for (let attempt = 1; attempt <= 3 && !publishedUrl; attempt++) {
        const clicked = await clickByText(page, ['List it', 'List item', 'Publish', 'Submit listing'], 6000);
        if (!clicked) { log('publish control not found'); break; }
        // allow either a success redirect/banner or an error render — whichever lands first
        const ok = () => publishSucceeded(page);
        await until(page, async () => (await ok()) || (await collectErrors(page)).length > 0, 4000, 200);
        if (await ok()) { publishedUrl = page.url(); break; }
        await snap(page, `6-blocked-${attempt}`);
        const errs = await collectErrors(page);
        log(`publish attempt ${attempt} blocked; errors=${JSON.stringify(errs).slice(0, 300)}`);
        // no errors AND no success — genuinely slow, so this one keeps a real grace period
        if (!errs.length) { await until(page, async () => (await ok()) || (await collectErrors(page)).length > 0, 2500, 200); continue; }
        const fixedAny = await resolveRequired(page, errs, payload, record);
        if (!fixedAny) {
          console.log(`PUBLISH_BLOCKED=${JSON.stringify(errs)}`);
          notify(`eBay listing BLOCKED: ${payload.title}\n${errs.join(' | ')}${draftId ? `\nresume: --draft-id ${draftId}` : ''}`);
          break;
        }
      }
      if (publishedUrl) {
        const itemId = (publishedUrl.match(/itemid=(\d+)/i) || [])[1] || null;
        const liveUrl = itemId ? 'https://www.ebay.com/itm/' + itemId : publishedUrl;
        await snap(page, '6-published');
        console.log(`PUBLISHED_URL=${liveUrl}`);
        log(`PUBLISHED url=${publishedUrl} itemId=${itemId} title=${JSON.stringify(payload.title)}`);
        notify(`eBay listing LIVE: ${payload.title}\n${payload.price != null ? '$' + payload.price + ' ' : ''}(${payload.format || 'auction'}) · ${payload.condition || ''}\n${liveUrl}`);
        return;
      }
      // Last-chance success check before we go anywhere near the draft path: the banner can land
      // late, and saving a draft on top of a live listing is how you end up with a duplicate.
      if (await publishSucceeded(page)) {
        await snap(page, '6-published');
        console.log(`PUBLISHED_URL=${page.url()}`);
        log(`PUBLISHED (late banner) url=${page.url()} title=${JSON.stringify(payload.title)}`);
        notify(`eBay listing LIVE: ${payload.title}\n${page.url()}`);
        return;
      }
      // couldn't publish cleanly — preserve the work as a draft and let the caller report why
      log('publish blocked after retries — falling back to draft save');
    }

    // default: save as draft
    const saved = await clickByText(page, ['Save for later', 'Save draft', 'Save and exit', 'Save'], 6000);
    if (!saved) {
      console.log('DRAFT_UNAVAILABLE');
      log('Save-for-later control not found — DRAFT_UNAVAILABLE');
      await snap(page, '6-no-save');
      return;
    }
    // draft saves redirect off the form; stop the moment that happens
    await until(page, async () => !/\/lstng/.test(page.url()), 4000, 200);
    await snap(page, '6-saved');
    // Best review link is the draft's own edit URL built from draftId (loads even after save,
    // and stays logged in). Fall back to the current URL, then the Sell hub.
    const url = draftId ? draftUrl(draftId)
              : (/lstng|\/sl\//i.test(page.url()) ? page.url() : DRAFTS_URL);
    console.log(`DRAFT_URL=${url}`);
    log(`DRAFT saved url=${url} | title=${JSON.stringify(payload.title)}`);
    notify(`eBay draft saved: ${payload.title}\n${url}${draftId ? `\nresume: --draft-id ${draftId}` : ''}`);
  } finally {
    await page.close().catch(() => {});
    await browser.close().catch(() => {});
  }
}

// ── main ───────────────────────────────────────────────────────────────────────
(async () => {
  const problems = validatePayload();

  if (DRY_RUN) {
    console.log('=== DRY RUN — nothing will touch eBay ===');
    console.log(`mode:      ${MODE}${RESUME_DRAFT_ID ? ` (RESUME draft ${RESUME_DRAFT_ID})` : ' (new prelist → new draft)'}`);
    console.log(`title:     ${payload.title}  (${payload.title ? [...payload.title].length : 0} chars)`);
    console.log(`price:     ${payload.price}  format: ${payload.format || '(default)'}`);
    console.log(`condition: ${payload.condition}${payload.conditionGrade ? ' / ' + payload.conditionGrade : ''}`);
    console.log(`specifics: ${Object.keys(payload.itemSpecifics || {}).join(', ') || '(none)'}`);
    console.log(`category:  ${payload.categoryId || '(let eBay choose)'}`);
    console.log(`photos:    ${photos.length}`);
    photos.forEach(p => { let ok = true; try { fs.accessSync(p); } catch { ok = false; } console.log(`           ${ok ? '✓' : '⚠️ MISSING'} ${p}`); });
    // CDP reachability
    let cdp = 'unreachable';
    try { const r = await fetch(`${CDP_URL}/json/version`, { signal: AbortSignal.timeout(3000) }); if (r.ok) cdp = 'reachable'; } catch {}
    console.log(`CDP:       ${cdp} (${CDP_URL})`);
    console.log(`config:    ${fs.existsSync(CONFIG_FILE) ? CONFIG_FILE : '(none — using built-in defaults)'}`);
    console.log(`           bestOffer=${CONFIG.bestOffer} notify=${CONFIG.notifyCommand ? 'on' : 'off'}`);
    console.log(problems.length ? `PROBLEMS:  ${problems.join('; ')}` : 'PROBLEMS:  none');
    log(`DRY-RUN mode=${MODE} title=${JSON.stringify(payload.title)} photos=${photos.length} problems=${problems.length}`);
    return;
  }

  if (problems.length) {
    console.error(`Payload problems (fix before a real run): ${problems.join('; ')}`);
    process.exit(1);
  }

  try { await run(); }
  catch (e) { log(`ERROR ${e.message}`); console.error(`ERROR ${e.message}`); process.exit(1); }
})();

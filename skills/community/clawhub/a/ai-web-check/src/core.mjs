const MAX_BODY_BYTES = 2_000_000;
const CHECK_ORDER = ['find', 'read', 'understand', 'navigate', 'act', 'verify', 'parity', 'safety'];
const STATUS = { PASS: 'PASS', WARN: 'WARN', FAIL: 'FAIL', NOT_APPLICABLE: 'NOT_APPLICABLE', NOT_TESTED: 'NOT_TESTED' };

function now() { return new Date().toISOString(); }
function stripTags(value) { return value.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim(); }
function absolute(base, value) { try { return new URL(value, base).href; } catch { return null; } }
function sameOrigin(base, value) { try { return new URL(base).origin === new URL(value).origin; } catch { return false; } }
function statusFor(condition, pass = STATUS.PASS, fail = STATUS.WARN) { return condition ? pass : fail; }

export async function fetchEvidence(url, { timeoutMs = 10_000, signal } = {}) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  const abort = () => controller.abort();
  signal?.addEventListener('abort', abort, { once: true });
  try {
    const response = await fetch(url, { redirect: 'follow', signal: controller.signal, headers: { accept: 'text/html,application/xhtml+xml,text/plain;q=0.9,*/*;q=0.1', 'user-agent': 'AIWebsiteCheck/0.1 (+read-only assessment)' } });
    const contentType = response.headers.get('content-type') || '';
    const body = await response.text();
    return { url: response.url, requestedUrl: url, status: response.status, ok: response.ok, contentType, body: body.slice(0, MAX_BODY_BYTES), truncated: body.length > MAX_BODY_BYTES };
  } catch (error) {
    return { url, requestedUrl: url, status: null, ok: false, contentType: '', body: '', error: error.name === 'AbortError' ? 'timeout' : error.message };
  } finally { clearTimeout(timer); signal?.removeEventListener('abort', abort); }
}

function count(pattern, html) { return [...html.matchAll(pattern)].length; }
function hasLabeledForms(html) {
  const controls = [...html.matchAll(/<(input|select|textarea)\b([^>]*)>/gi)];
  if (!controls.length) return null;
  return controls.every((match) => {
    const id = /\bid\s*=\s*["']([^"']+)["']/i.exec(match[2])?.[1];
    const aria = /\baria-label(?:ledby)?\s*=\s*["'][^"']+['"]/i.test(match[2]);
    return aria || (id && new RegExp(`<label[^>]*for\\s*=\\s*["']${escapeRegExp(id)}["']`, 'i').test(html));
  });
}
function escapeRegExp(value) { return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
function check(id, label, status, evidence, remediation) { return { id, label, status, evidence, remediation }; }

export function inspectHtml(page, discovery) {
  const html = page.body;
  const title = /<title\b[^>]*>([\s\S]*?)<\/title>/i.exec(html)?.[1] || '';
  const headings = count(/<h[1-6]\b[^>]*>/gi, html);
  const main = /<main\b/i.test(html) || /\brole\s*=\s*["']main["']/i.test(html);
  const nav = /<nav\b/i.test(html) || /\brole\s*=\s*["']navigation["']/i.test(html);
  const images = [...html.matchAll(/<img\b([^>]*)>/gi)];
  const imagesWithAlt = images.filter((m) => /\balt\s*=\s*["'][^"']*["']/i.test(m[1])).length;
  const buttons = [...html.matchAll(/<(button|a)\b([^>]*)>([\s\S]*?)<\/\1>/gi)];
  const namedButtons = buttons.filter((m) => stripTags(m[3]) || /aria-label\s*=/i.test(m[2])).length;
  const actionIds = count(/\bdata-action-id\s*=/gi, html);
  const labeledForms = hasLabeledForms(html);
  const hasStructuredData = /application\/ld\+json/i.test(html);
  const hasCanonical = /<link[^>]+rel\s*=\s*["']canonical["']/i.test(html);
  const hasStatus = /\b(role\s*=\s*["'](status|alert)["']|aria-live\s*=)/i.test(html);
  const linkCount = count(/<a\b[^>]+href\s*=/gi, html);
  const actionWords = /\b(submit|send|pay|purchase|delete|confirm|place order)\b/i.test(stripTags(html));

  return [
    check('find', 'Find', statusFor(page.ok && Boolean(title) && linkCount > 0), [`HTTP ${page.status ?? 'network error'}; title=${Boolean(title)}; links=${linkCount}; canonical=${hasCanonical}; robots=${discovery.robots.status}; sitemap=${discovery.sitemap.status}; llms=${discovery.llms.status}`], 'Expose stable public entry points, canonical URLs, and a sitemap; publish llms.txt only when it is maintained.'),
    check('read', 'Read', statusFor(headings > 0 && main && (images.length === imagesWithAlt), STATUS.PASS, STATUS.WARN), [`headings=${headings}; main=${main}; nav=${nav}; imagesWithAlt=${imagesWithAlt}/${images.length}; labeledForms=${labeledForms ?? 'n/a'}`], 'Use semantic landmarks and headings, text alternatives, and visible labels linked to every form control.'),
    check('understand', 'Understand', statusFor(hasStructuredData || actionIds > 0, STATUS.PASS, STATUS.WARN), [`structuredData=${hasStructuredData}; dataActionIds=${actionIds}; namedControls=${namedButtons}/${buttons.length}`], 'Give important actions stable machine identifiers and disclose action intent/effect, not only short visual button text.'),
    check('navigate', 'Navigate', statusFor(linkCount > 0 && nav, STATUS.PASS, STATUS.WARN), [`links=${linkCount}; navigationLandmark=${nav}; onlyStaticInspection=true`], 'Add a clear navigation landmark and test declared public GET-only journeys separately.'),
    check('act', 'Act', STATUS.NOT_TESTED, [`formControls=${labeledForms === null ? 0 : 'present'}; riskyActionLanguage=${actionWords}; runner=read-only`], 'Test creates/updates only in a sandbox with explicit fixtures, idempotency keys, and confirmation boundaries.'),
    check('verify', 'Verify', hasStatus ? STATUS.WARN : STATUS.NOT_TESTED, [`persistentStatusRegion=${hasStatus}; noBusinessReceiptObserved=true`], 'Return an independent, machine-readable receipt with resource ID, state, version, and follow-up link.'),
    check('parity', 'Parity', STATUS.NOT_TESTED, ['No API/MCP/WebMCP or shared-state evidence was supplied to this read-only scan.'], 'Compare human and machine routes against one action core and the same observed business state.'),
    check('safety', 'Safety', actionWords ? STATUS.WARN : STATUS.NOT_TESTED, [`riskyActionLanguage=${actionWords}; noAuthenticatedOrMutatingTest=true`], 'Use explicit confirmation, authorization, idempotency, expected-state-version, and safe human handoff for side effects.')
  ];
}

export async function scan(url, options = {}) {
  let target;
  try { target = new URL(url); } catch { throw new Error('URL must be an absolute http(s) URL.'); }
  if (!['http:', 'https:'].includes(target.protocol)) throw new Error('URL must use http or https.');
  const page = await fetchEvidence(target.href, options);
  const root = new URL(page.url || target.href).origin;
  const [robots, sitemap, llms] = await Promise.all(['robots.txt', 'sitemap.xml', 'llms.txt'].map((path) => fetchEvidence(new URL(`/${path}`, root).href, options)));
  const checks = inspectHtml(page, { robots, sitemap, llms });
  const read = checks.find((item) => item.id === 'read');
  return { schemaVersion: 'ai-web-check/v0.1', generatedAt: now(), target: { requestedUrl: target.href, finalUrl: page.url, readOnly: true }, profiles: { static: page.ok ? STATUS.PASS : STATUS.FAIL, accessibility: read.status, browser: STATUS.NOT_TESTED, computerUse: STATUS.NOT_TESTED, jev: STATUS.NOT_TESTED, mcp: STATUS.NOT_TESTED, webmcp: STATUS.NOT_TESTED, actionParity: STATUS.NOT_TESTED }, checks, evidence: { page: summarize(page), discovery: { robots: summarize(robots), sitemap: summarize(sitemap), llms: summarize(llms) } } };
}
function summarize(item) { return { requestedUrl: item.requestedUrl, finalUrl: item.url, status: item.status, ok: item.ok, contentType: item.contentType, truncated: item.truncated || false, error: item.error || null }; }

export async function runJourney(baseUrl, definition, options = {}) {
  if (!definition || !Array.isArray(definition.steps) || !definition.steps.length) throw new Error('Journey JSON must contain a non-empty steps array.');
  const base = new URL(baseUrl);
  const steps = await Promise.all(definition.steps.map(async (step) => {
    const url = absolute(base.href, step);
    if (!url || !sameOrigin(base.href, url)) return { requested: step, status: STATUS.FAIL, error: 'Journey step must be a same-origin URL.' };
    const response = await fetchEvidence(url, options);
    return { requested: step, finalUrl: response.url, httpStatus: response.status, status: response.ok ? STATUS.PASS : STATUS.FAIL, error: response.error || null };
  }));
  return { schemaVersion: 'ai-web-check/journey/v0.1', generatedAt: now(), target: base.href, name: definition.name || 'Unnamed read-only journey', safety: 'GET-only; no JavaScript execution, authentication, form input, or side effect.', status: steps.every((step) => step.status === STATUS.PASS) ? STATUS.PASS : STATUS.FAIL, steps };
}

export function toMarkdown(report) {
  const lines = [`# AI Website Check`, '', `- Schema: \`${report.schemaVersion}\``, `- Generated: ${report.generatedAt}`, `- Target: ${report.target?.finalUrl || report.target}`, `- Mode: read-only`, '', '## Checks', '', '| Layer | Status | Evidence |', '| --- | --- | --- |'];
  if (report.checks) for (const item of report.checks) lines.push(`| ${item.label} | **${item.status}** | ${item.evidence.join('; ').replace(/\|/g, '\\|')} |`);
  if (report.steps) { lines.push('', `## ${report.name}`, '', `Overall: **${report.status}**`, '', '| Step | Status | HTTP |', '| --- | --- | --- |'); for (const step of report.steps) lines.push(`| ${step.requested} | **${step.status}** | ${step.httpStatus ?? step.error} |`); }
  lines.push('', '## Boundary', '', report.safety || 'This result is evidence for the named checks only. NOT_TESTED is not a pass; this is not a security scan or vendor certification.');
  return `${lines.join('\n')}\n`;
}

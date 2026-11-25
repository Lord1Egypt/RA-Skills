import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const sha = /^[a-f0-9]{40}$/;
const digest = /^[a-f0-9]{64}$/;
export function validate(r) {
  const fail = () => { throw new Error('Invalid custom-build report'); };
  const keys = (v, names) => {
    if (!v || Array.isArray(v) || typeof v !== 'object' ||
        Object.keys(v).length !== names.length || names.some(k => !(k in v))) fail();
  };
  const text = v => typeof v === 'string' && v.trim().length > 0 && v.length <= 4000;
  keys(r, ['schema','runId','baseSha','candidateSha','candidateTree','patches','result','cleanup','tests','artifacts','summary']);
  if (r.schema !== 'openclaw.custom-build-report/v1' ||
      !/^[a-f0-9]{8}-(?:[a-f0-9]{4}-){3}[a-f0-9]{12}$/.test(r.runId) ||
      ![r.baseSha,r.candidateSha,r.candidateTree].every(x => typeof x === 'string' && sha.test(x)) ||
      !Array.isArray(r.patches) || r.patches.length > 100 || !r.patches.every(x => typeof x === 'string' && sha.test(x)) ||
      !['passed','failed','blocked','not-evaluated'].includes(r.result) ||
      !['complete','retained','failed','not-required'].includes(r.cleanup) || !text(r.summary) ||
      !Array.isArray(r.tests) || r.tests.length > 100 || !Array.isArray(r.artifacts) || r.artifacts.length > 100) fail();
  for (const t of r.tests) {
    keys(t, ['surface','result','proof']);
    if (!text(t.surface) || !['passed','failed','blocked'].includes(t.result) ||
        !['source','automated','runtime','human'].includes(t.proof)) fail();
  }
  for (const a of r.artifacts) {
    keys(a, ['component','sha256','platform']);
    if (!text(a.component) || !text(a.platform) || typeof a.sha256 !== 'string' || !digest.test(a.sha256)) fail();
  }
  if (r.result === 'passed' && (!r.tests.length || r.tests.some(t => t.result !== 'passed'))) fail();
  if (r.tests.some(t => t.result === 'failed') && r.result !== 'failed') fail();
  if (r.result === 'not-evaluated' && r.tests.length) fail();
  return r;
}
const escapeHtml = s => s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
export function render(value) {
  const r = validate(value);
  const json = JSON.stringify(r).replaceAll('<','\\u003c').replaceAll('>','\\u003e').replaceAll('&','\\u0026');
  const body = `## Custom build validation\n\nBase: \`${r.baseSha}\`\nCandidate: \`${r.candidateSha}\`\nTree: \`${r.candidateTree}\`\nResult: **${r.result}**\nCleanup: ${r.cleanup}\n\n${escapeHtml(r.summary)}\n\n` +
    r.tests.map(t => `- ${escapeHtml(t.surface)}: ${t.result} (${t.proof})`).join('\n') +
    `\n\n<!-- openclaw-custom-build-report:v1\n${json}\n-->\n`;
  if (Buffer.byteLength(body, 'utf8') >= 60000) throw new Error('Comment exceeds UTF-8 byte limit');
  return body;
}
if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  try {
    if (process.argv.length !== 3) throw new Error('Usage: node report.mjs sanitized-export.json');
    const raw = readFileSync(process.argv[2], 'utf8');
    if (Buffer.byteLength(raw) > 1000000) throw new Error('Report input too large');
    process.stdout.write(render(JSON.parse(raw)));
  } catch (e) { console.error(e.message); process.exitCode = 1; }
}

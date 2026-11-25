#!/usr/bin/env node
// smoke-test.js — offline end-to-end test of the skill. No real websites are contacted:
// it starts tiny local HTTP servers on 127.0.0.1 and scrapes those.
// Run: npm test    (or: node scripts/smoke-test.js)
// Covers: self-test, input validation, scrape + CSV columns, suspicious detection,
//         429 block handling, interrupt → resume (no re-fetching), --fresh archiving.

const http = require('http');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawn, spawnSync } = require('child_process');
const { parse } = require('csv-parse/sync');

const SCRAPER = path.join(__dirname, 'email-scraper.js');
const VALIDATE = path.join(__dirname, 'validate-input.js');
const SUMMARY = path.join(__dirname, 'summarize-run.js');
const EXPECTED_COLUMNS = ['url','business_name','email','phone','email_count','email_source','confidence','suspicious','notes','source_page','fb_page_url','channel','status','error','scraped_at'];

let passed = 0, failed = 0;
const ok = (cond, msg) => { if (cond) { passed++; console.log('  PASS ' + msg); } else { failed++; console.log('  FAIL ' + msg); } };
const run = (file, args, opts = {}) => spawnSync(process.execPath, [file, ...args], { encoding: 'utf8', ...opts });
// NOTE: scraper runs that hit the local fake sites MUST be async — spawnSync would block this
// process's event loop, and the fake servers live in this process.
const runA = (file, args) => new Promise(resolve => {
  const c = spawn(process.execPath, [file, ...args], { stdio: ['ignore', 'pipe', 'pipe'] });
  let stdout = '', stderr = '';
  c.stdout.on('data', d => stdout += d); c.stderr.on('data', d => stderr += d);
  c.on('exit', status => resolve({ status, stdout, stderr }));
});

// ---- local fake sites (one port per site so block-tracking is per site) ----
const hits = {};
function startSite(name, handler) {
  hits[name] = 0;
  return new Promise(res => {
    const s = http.createServer((req, rsp) => { hits[name]++; handler(req, rsp); });
    s.listen(0, '127.0.0.1', () => res({ name, server: s, url: `http://127.0.0.1:${s.address().port}` }));
  });
}
const html = (rsp, body, code = 200) => { rsp.writeHead(code, { 'Content-Type': 'text/html' }); rsp.end(body); };

async function main() {
  const sites = await Promise.all([
    startSite('A_mailto',   (q, r) => q.url === '/' ? html(r, '<a href="mailto:info@alphabakery.test">Mail us</a><p>Call 212-555-0143</p>') : html(r, 'nope', 404)),
    startSite('B_contact',  (q, r) => q.url === '/contact' ? html(r, '<p>Write to sales [at] gammaroofing [dot] test</p>') : html(r, '<p>Welcome</p>', q.url === '/' ? 200 : 404)),
    startSite('C_none',     (q, r) => html(r, q.url === '/' ? '<p>No contact info here</p>' : 'nope', q.url === '/' ? 200 : 404)),
    startSite('D_blocked',  (q, r) => html(r, 'Too Many Requests', 429)),
    startSite('E_typo',     (q, r) => q.url === '/' ? html(r, '<a href="mailto:hello@bangbangpie.con">hi</a>') : html(r, 'nope', 404)),
  ]);
  const byName = Object.fromEntries(sites.map(s => [s.name, s]));
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'leadskill-'));
  const csvOf = urls => 'url\n' + urls.join('\n') + '\n';

  try {
    console.log('\n[1] self-test');
    const st = run(SCRAPER, ['--selftest']);
    const m = /(\d+)\/(\d+) normalizeEmail cases passed/.exec(st.stdout);
    ok(st.status === 0 && m && Number(m[1]) >= 7, `selftest ran (${m ? m[0] : 'no summary'}; 7/8 is the known baseline of the original script)`);

    console.log('\n[2] validate-input');
    fs.writeFileSync(path.join(tmp, 'bad.csv'), 'name,phone\nBob,123\n');
    ok(run(VALIDATE, [path.join(tmp, 'bad.csv')]).status === 2, 'CSV without URL column → exit 2');
    fs.writeFileSync(path.join(tmp, 'mixed.csv'), 'website\nexample.org\nhttps://example.org/\nnot a url\nftp://x.com\nhttp://localhost:3000\nhttp://192.168.1.5\nhttps://www.facebook.com/somebiz\nhttpbin.org\n');
    const v = run(VALIDATE, [path.join(tmp, 'mixed.csv'), '--write-clean', path.join(tmp, 'clean.csv')]);
    ok(v.status === 0 && /Valid \(unique\)  : 3/.test(v.stdout), 'mixed list: 3 valid (example.org, facebook page, httpbin.org)');
    ok(/Duplicates      : 1/.test(v.stdout), 'duplicate detected');
    ok(/Invalid         : 4/.test(v.stdout), 'invalid/private/ftp rejected (4)');
    const clean = parse(fs.readFileSync(path.join(tmp, 'clean.csv'), 'utf8'), { columns: true });
    ok(clean.every(r => /^https?:\/\//.test(r.url)), 'bare domains get https:// in clean file (httpbin.org is the original’s startsWith("http") pitfall)');
    ok(run(VALIDATE, [path.join(tmp, 'mixed.csv'), '--write-clean', path.join(tmp, 'clean.csv')]).status === 2, 'refuses to overwrite existing clean file');
    ok(/social-media/.test(v.stdout), 'warns about social-media URL');

    console.log('\n[3] scraper input handling');
    const wd0 = path.join(tmp, 'wd0');
    ok(run(SCRAPER, ['--workdir', wd0]).status === 2, 'missing input.csv → exit 2');
    fs.writeFileSync(path.join(wd0, 'input.csv'), 'name\nx\n');
    ok(run(SCRAPER, ['--workdir', wd0]).status === 2, 'no url column → exit 2');
    fs.writeFileSync(path.join(wd0, 'input.csv'), 'url\n');
    ok(run(SCRAPER, ['--workdir', wd0]).status === 2, 'header only (no rows) → exit 2, no crash');

    console.log('\n[4] full run on local sites');
    const wd1 = path.join(tmp, 'run1');
    fs.mkdirSync(wd1);
    const urls = ['A_mailto','B_contact','C_none','D_blocked','E_typo'].map(n => byName[n].url);
    fs.writeFileSync(path.join(wd1, 'input.csv'), csvOf(urls));
    const r1 = await runA(SCRAPER, ['--workdir', wd1, '--concurrency', '1']);
    ok(r1.status === 0 && /RUN COMPLETE/.test(r1.stdout), 'scraper exits 0 with RUN COMPLETE');
    ok(!/\x1b\[/.test(r1.stdout), 'plain output (no ANSI codes) by default');
    const out = parse(fs.readFileSync(path.join(wd1, 'output.csv'), 'utf8'), { columns: true });
    ok(JSON.stringify(Object.keys(out[0])) === JSON.stringify(EXPECTED_COLUMNS), 'output.csv has the original 15 columns in order');
    const rowFor = n => out.find(r => r.url === byName[n].url);
    ok(rowFor('A_mailto').email === 'info@alphabakery.test' && rowFor('A_mailto').email_source === 'mailto' && rowFor('A_mailto').status === 'found', 'A: mailto email found');
    ok(rowFor('B_contact').email === 'sales@gammaroofing.test' && rowFor('B_contact').email_source === 'deobfuscated', 'B: [at]/[dot] email found on /contact');
    ok(rowFor('C_none').status === 'not_found' && rowFor('C_none').email === '', 'C: no email → not_found (nothing invented)');
    ok(rowFor('D_blocked').status === 'blocked' && /429/.test(rowFor('D_blocked').error), 'D: HTTP 429 → status=blocked with reason');
    ok(hits.D_blocked <= 2, `D: blocking site not hammered (${hits.D_blocked} request(s))`);
    ok(rowFor('E_typo').status === 'not_found', 'E: typo-TLD email not placed in clean output');
    const susp = parse(fs.readFileSync(path.join(wd1, 'suspicious.csv'), 'utf8'), { columns: true });
    ok(susp.length === 1 && susp[0].email === 'hello@bangbangpie.con' && /suspicious-tld/.test(susp[0].reason), 'E: flagged in suspicious.csv, not auto-corrected');
    const cache = JSON.parse(fs.readFileSync(path.join(wd1, 'cache.json'), 'utf8'));
    ok(urls.every(u => Array.isArray(cache[u])), 'cache.json holds row arrays for every URL');
    const sm = run(SUMMARY, ['--workdir', wd1, '--json']);
    const sj = JSON.parse(sm.stdout).summary;
    ok(sj.found === 2 && sj.not_found === 2 && sj.blocked === 1 && sj.pending_not_yet_processed === 0, 'summarize-run: found 2 / not_found 2 / blocked 1 / pending 0');

    console.log('\n[5] interrupt → resume');
    const wd2 = path.join(tmp, 'run2');
    fs.mkdirSync(wd2);
    const urls2 = ['A_mailto','B_contact','C_none','E_typo'].map(n => byName[n].url);
    fs.writeFileSync(path.join(wd2, 'input.csv'), csvOf(urls2));
    const hitsA0 = hits.A_mailto;
    await new Promise(resolve => {
      const child = spawn(process.execPath, [SCRAPER, '--workdir', wd2, '--concurrency', '1'], { stdio: ['ignore', 'pipe', 'pipe'] });
      let buf = '', killed = false;
      child.stdout.on('data', d => {
        buf += d;
        if (!killed && /PROGRESS 1\/4/.test(buf)) { killed = true; child.kill(process.platform === 'win32' ? undefined : 'SIGINT'); }
      });
      child.on('exit', resolve);
    });
    const partial = JSON.parse(fs.readFileSync(path.join(wd2, 'cache.json'), 'utf8'));
    const done1 = Object.keys(partial).length;
    ok(done1 >= 1 && done1 < 4, `interrupted run left a valid checkpoint (${done1}/4 URLs cached)`);
    const sPart = JSON.parse(run(SUMMARY, ['--workdir', wd2, '--json']).stdout).summary;
    ok(sPart.can_resume === true && sPart.pending_not_yet_processed === 4 - done1, 'summarize-run reports pending URLs and can_resume=true');
    const hitsAmid = hits.A_mailto;
    const r2 = await runA(SCRAPER, ['--workdir', wd2, '--concurrency', '1']);
    ok(new RegExp(`Resume from  : ${done1} already done`).test(r2.stdout), `resume announces "${done1} already done"`);
    ok(r2.status === 0 && /RUN COMPLETE/.test(r2.stdout), 'resumed run completes');
    ok(hits.A_mailto === hitsAmid, 'already-scraped site A was NOT requested again after resume');
    const out2 = parse(fs.readFileSync(path.join(wd2, 'output.csv'), 'utf8'), { columns: true });
    ok(new Set(out2.map(r => r.url)).size === 4, 'final output.csv covers all 4 URLs (restored + new)');

    console.log('\n[6] --fresh archives instead of deleting');
    const r3 = await runA(SCRAPER, ['--workdir', wd2, '--concurrency', '1', '--fresh']);
    const files = fs.readdirSync(wd2);
    ok(/Resume from  : 0 already done/.test(r3.stdout), '--fresh starts from 0');
    ok(files.some(f => /^output_archived_.*\.csv$/.test(f)) && files.some(f => /^cache_archived_.*\.json$/.test(f)), 'previous output/cache archived with timestamp, not deleted');

    console.log('\n[7] no credentials / secrets left in skill');
    const scraperSrc = fs.readFileSync(SCRAPER, 'utf8');
    ok(!/FB_PASSWORD|FB_EMAIL|puppeteer/i.test(scraperSrc), 'no Facebook login code, no puppeteer, no hardcoded credentials');
  } finally {
    sites.forEach(s => s.server.close());
    fs.rmSync(tmp, { recursive: true, force: true });
  }
  console.log(`\n${passed} passed, ${failed} failed`);
  process.exit(failed ? 1 : 0);
}
main().catch(e => { console.error(e); process.exit(1); });

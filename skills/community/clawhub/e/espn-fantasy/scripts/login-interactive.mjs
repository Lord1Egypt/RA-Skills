// Live ESPN login: handles 2FA email codes + auto-backs off on ESPN code-send rate limits.
import fs from 'fs';
import path from 'path';
import { launch, SECRETS } from './lib.mjs';

const WS = path.join(process.env.HOME, '.openclaw/workspace');
const ST = path.join(WS, 'state');
const CODE_FILE = path.join(ST, 'espn-2fa-code.txt');
const LOG = path.join(ST, 'espn-login.log');
const SHOT = path.join(ST, 'espn-live.png');
const log = (m) => { const l = `[${new Date().toISOString()}] ${m}`; console.log(l); fs.appendFileSync(LOG, l + '\n'); };
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

try { fs.unlinkSync(CODE_FILE); } catch {}
fs.writeFileSync(LOG, '');

const txt = fs.readFileSync(SECRETS, 'utf8');
const user = (txt.match(/^ESPN_USER\s*=\s*(.+)$/m) || [])[1].trim();
const pass = (txt.match(/^ESPN_PASS\s*=\s*(.+)$/m) || [])[1].trim();

const ctx = await launch();
const page = ctx.pages()[0] || await ctx.newPage();
const getFrame = () => page.frames().find(f => /registerdisney/.test(f.url()) && f.name() === 'disneyid-iframe');
const frameText = async (f) => { try { return (await f.evaluate(() => document.body ? document.body.innerText.replace(/\s+/g, ' ').trim() : '')).slice(0, 220); } catch { return ''; } };
const hasS2 = async () => !!(await ctx.cookies()).find(c => c.name === 'espn_s2');

async function saveCookies() {
  const cookies = await ctx.cookies();
  const s2 = cookies.find(c => c.name === 'espn_s2');
  const swid = cookies.find(c => c.name === 'SWID');
  if (s2 && swid) {
    fs.writeFileSync(path.join(WS, '.secrets/espn-cookies.txt'),
      'espn_s2=' + s2.value + '\nSWID=' + swid.value + '\n', { mode: 0o600 });
    log('SUCCESS espn_s2+SWID saved');
    return true;
  }
  return false;
}

async function doLogin() {
  log('goto login');
  await page.goto('https://www.espn.com/login', { waitUntil: 'domcontentloaded', timeout: 45000 });
  let frame = null;
  for (let i = 0; i < 20 && !frame; i++) { await sleep(1500); frame = getFrame(); }
  await frame.waitForSelector('input[type=email]', { timeout: 30000 });
  await frame.fill('input[type=email]', user);
  await frame.fill('input[type=password]', pass);
  log('submit creds');
  await frame.click('button[type=submit]');
  await sleep(8000);
}

try {
  const hardDeadline = Date.now() + 120 * 60 * 1000; // 120 min total budget
  let done = false;

  for (let attempt = 1; attempt <= 6 && !done && Date.now() < hardDeadline; attempt++) {
    await doLogin();
    // observe up to ~10 min for: success / code prompt / rate-limit
    let outcome = 'timeout';
    for (let i = 0; i < 200; i++) {
      if (await hasS2()) { outcome = 'success'; break; }
      const f = getFrame();
      const text = f ? await frameText(f) : '';
      if (i % 5 === 0) { try { await page.screenshot({ path: SHOT }); } catch {} }
      if (/Check Your Email|sent a code|Enter the code/i.test(text)) { outcome = 'prompt'; break; }
      if (/unable to send you any more codes/i.test(text)) { outcome = 'ratelimit'; break; }
      await sleep(3000);
    }

    if (outcome === 'success') { await saveCookies(); done = true; break; }
    if (outcome === 'ratelimit') {
      log('RATE_LIMITED attempt ' + attempt + '; backing off 12 min');
      try { const ok = await getFrame().$('button, a'); } catch {}
      await sleep(12 * 60 * 1000);
      continue;
    }
    if (outcome === 'timeout') { log('TIMEOUT attempt ' + attempt + '; retrying'); await sleep(30000); continue; }

    if (outcome === 'prompt') {
      log('2FA_PROMPT active. waiting for code file: ' + CODE_FILE);
      // wait up to 45 min for a code to be dropped
      const codeDeadline = Date.now() + 45 * 60 * 1000;
      let submitted = false;
      while (Date.now() < codeDeadline) {
        if (await hasS2()) { done = true; break; }
        if (fs.existsSync(CODE_FILE)) {
          const code = fs.readFileSync(CODE_FILE, 'utf8').trim();
          try { fs.unlinkSync(CODE_FILE); } catch {}
          log('CODE_SUBMIT ' + code);
          try {
            const f = getFrame();
            const inp = (await f.$('input[name=code]')) || (await f.$('input[type=tel]'));
            await inp.fill(code);
            await (await f.$('button[type=submit]')).click();
            await sleep(10000);
            const nf = getFrame() || f;
            log('AFTER_CODE frame="' + (await frameText(nf)) + '" url=' + page.url());
            submitted = true;
          } catch (e) { log('CODE_SUBMIT_ERR ' + e.message); }
        }
        // after submit, give it time then decide
        if (submitted) {
          await sleep(8000);
          if (await hasS2()) { done = true; break; }
          const t = await frameText(getFrame() || { evaluate: async () => '' });
          if (/unable to send|incorrect|expired|invalid|try again/i.test(t)) { log('CODE_REJECTED "' + t.slice(0,120) + '"'); break; }
          // if still on prompt and not rejected, keep waiting a bit more
        }
        await sleep(3000);
      }
      if (done) break;
      log('code phase ended without success; retrying login');
      continue;
    }
  }

  const ok = await saveCookies();
  log('DONE url=' + page.url() + ' success=' + ok);
} catch (e) { log('ERROR ' + e.message); }
finally { await ctx.close(); }

// Shared ESPN browser helpers
import { fileURLToPath } from 'url';
import path from 'path';
// playwright: prefer a local install; fall back to PLAYWRIGHT_PATH env, then a common path.
export const PLAYWRIGHT = process.env.PLAYWRIGHT_PATH || 'playwright';
export const PROFILE = process.env.ESPN_PROFILE || path.join(process.env.HOME, '.openclaw/workspace/state/espn-profile');
export const SECRETS = process.env.ESPN_SECRETS || path.join(process.env.HOME, '.openclaw/workspace/.secrets/espn-login.txt');
export const { chromium } = await import(PLAYWRIGHT);

export async function launch() {
  const headed = process.env.HEADED === '1';
  const fullChrome = process.env.FULLCHROME === '1';
  const opts = {
    headless: !headed,
    args: ['--no-sandbox', '--disable-blink-features=AutomationControlled'],
    viewport: { width: 1366, height: 900 },
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
  };
  if (fullChrome && !headed) {
    // Full Chromium build in new-headless mode (closer to real browser than headless_shell)
    opts.headless = false;
    opts.executablePath = process.env.HOME + '/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome';
    opts.args.push('--headless=new', '--hide-scrollbars', '--mute-audio');
  }
  const ctx = await chromium.launchPersistentContext(PROFILE, opts);
  await ctx.addInitScript(() => { Object.defineProperty(navigator, 'webdriver', { get: () => undefined }); });
  return ctx;
}

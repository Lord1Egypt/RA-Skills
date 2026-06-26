/**
 * browser.mjs — Browser factory
 * Creates Kernel stealth browsers for all operations
 */
import { KERNEL_SDK_PATH, DEFAULT_PLAYWRIGHT_PATH } from './constants.mjs';

let _chromium;
async function getChromium(playwrightPath) {
  if (_chromium) return _chromium;
  const paths = [playwrightPath, DEFAULT_PLAYWRIGHT_PATH, 'playwright'].filter(Boolean);
  for (const p of paths) {
    try { const m = await import(p); _chromium = m.chromium; return _chromium; } catch {}
  }
  throw new Error('Playwright not found — install with: npm install -g playwright');
}

export async function createBrowser(settings, profileNameOrKey) {
  const kernelConfig = settings.kernel || {};
  const playwrightPath = settings.browser?.playwright_path;
  const apiKey = process.env.KERNEL_API_KEY || settings.kernel_api_key;

  if (!apiKey) throw new Error('KERNEL_API_KEY not set');

  let Kernel;
  try {
    const mod = await import(KERNEL_SDK_PATH);
    Kernel = mod.default;
  } catch {
    throw new Error('Kernel SDK not installed — run: npm install @onkernel/sdk');
  }

  const kernel = new Kernel({ apiKey });

  // Accept either a profile name directly or a platform key (legacy fallback)
  let profileName = profileNameOrKey;
  if (profileName && kernelConfig.profiles?.[profileName]) {
    profileName = kernelConfig.profiles[profileName];
  }

  const opts = { stealth: true };
  if (profileName) opts.profile = { name: profileName };

  // Proxy: look up by name "claw-apply", create if missing
  try {
    for await (const proxy of kernel.proxies.list()) {
      if (proxy.name === 'claw-apply' && proxy.status === 'available') {
        opts.proxy = { id: proxy.id };
        break;
      }
    }
    if (!opts.proxy) {
      const newProxy = await kernel.proxies.create({ name: 'claw-apply', type: 'residential', country: 'US' });
      opts.proxy = { id: newProxy.id };
    }
  } catch {}

  let kb;
  try {
    kb = await kernel.browsers.create(opts);
  } catch (e) {
    throw new Error(`Kernel browser creation failed: ${e.message}`);
  }
  const pw = await getChromium(playwrightPath);
  let browser;
  try {
    browser = await pw.connectOverCDP(kb.cdp_ws_url);
  } catch (e) {
    throw new Error(`CDP connection failed (browser ${kb.id}): ${e.message}`);
  }
  const ctx = browser.contexts()[0] || await browser.newContext();
  const page = ctx.pages()[0] || await ctx.newPage();

  return { browser, page, type: 'kernel', kernel, kernelBrowserId: kb.id };
}

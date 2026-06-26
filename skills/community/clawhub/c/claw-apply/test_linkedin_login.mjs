import { createBrowser } from './lib/browser.mjs';
import { verifyLogin } from './lib/linkedin.mjs';
import { loadConfig } from './lib/queue.mjs';
import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';

const __dir = dirname(fileURLToPath(import.meta.url));
const settings = loadConfig(resolve(__dir, 'config/settings.json'));

let browser;
try {
  console.log('Creating Kernel browser with LinkedIn profile...');
  browser = await createBrowser(settings, 'linkedin');
  console.log('Browser created, checking login...');
  const loggedIn = await verifyLogin(browser.page);
  console.log('Logged in:', loggedIn);
  console.log('URL:', browser.page.url());
} catch (e) {
  console.error('Error:', e.message);
  process.exit(1);
} finally {
  await browser?.browser?.close().catch(() => {});
  console.log('Done.');
}

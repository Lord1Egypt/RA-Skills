# Playwright recipes for Oganim verification

These are battle-tested probes used to verify deploys. Drop into `/tmp/oganim-test/`.

## Setup (once per server)

```bash
mkdir -p /tmp/oganim-test && cd /tmp/oganim-test
npm init -y >/dev/null && npm i playwright --no-save

# Playwright pins a browser version; symlink existing cache so the install
# doesn't have to download Chromium again. Adjust 1217/1223 to whatever
# is in `ls ~/.cache/ms-playwright/`.
ln -sfn ~/.cache/ms-playwright/chromium_headless_shell-1217 \
        ~/.cache/ms-playwright/chromium_headless_shell-1223 2>/dev/null
```

## Recipe 1 — verify a magic-link lands in the portal

Generates a real magic link for a customer via admin API and follows it.
Use for any change touching `api/send-portal-link.js`, `index.html` bridge,
or `portal/portal.js` magic-link handler.

```js
const fs = require('fs');
const { chromium } = require('playwright');
const cred = Object.fromEntries(
  fs.readFileSync(process.env.HOME + '/.openclaw/credentials/supabase/credentials.env', 'utf8')
    .split('\n').filter(l => l.includes('='))
    .map(l => { const i = l.indexOf('='); return [l.slice(0, i), l.slice(i + 1)]; })
);

(async () => {
  const email = process.argv[2] || 'shlomo@dfbdf.com';
  const gen = await fetch(`${cred.SUPABASE_URL}/auth/v1/admin/generate_link`, {
    method: 'POST',
    headers: {
      apikey: cred.SUPABASE_SERVICE_ROLE_KEY,
      Authorization: 'Bearer ' + cred.SUPABASE_SERVICE_ROLE_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ type: 'magiclink', email }),
  }).then(r => r.json());
  const url = `https://oganimy.co.il/portal/?token_hash=${gen.hashed_token}&type=magiclink`;

  const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
  const page    = await (await browser.newContext({ ignoreHTTPSErrors: true })).newPage();
  page.on('pageerror', e => console.log('[PAGEERROR]', e.message));

  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(3500);

  const stillOnLogin = await page.locator('input[type="password"]').first().isVisible().catch(() => false);
  console.log('login form visible (= auth FAILED):', stillOnLogin);
  console.log('current URL:', page.url());
  console.log('body excerpt:', (await page.locator('body').innerText()).slice(0, 300));

  await page.screenshot({ path: '/tmp/oganim-test/magic-link.png' });
  await browser.close();
})();
```

## Recipe 2 — verify FAB stacking on mobile

Catches CSS overlap regressions in the 3 floating buttons (WhatsApp, AI
chat, accessibility).

```js
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
  const page = await (await browser.newContext({
    viewport: { width: 412, height: 915 },
    ignoreHTTPSErrors: true,
  })).newPage();
  await page.goto('https://oganimy.co.il/', { waitUntil: 'networkidle' });
  await page.evaluate(() => window.scrollTo(0, 1500));
  await page.waitForTimeout(800);

  const rects = await page.evaluate(() => ['.wa-fab', '.ogc-fab', '.a11y-toggle'].map(s => {
    const el = document.querySelector(s);
    if (!el) return { sel: s, present: false };
    const r = el.getBoundingClientRect();
    return { sel: s, top: r.top, bottom: r.bottom, left: r.left };
  }));
  console.table(rects);

  // Assert: each fab's top must be ABOVE the next fab's bottom by >= 4px
  const sorted = rects.filter(r => r.present).sort((a, b) => a.top - b.top);
  for (let i = 1; i < sorted.length; i++) {
    const gap = sorted[i].top - sorted[i - 1].bottom;
    if (gap < 4) console.log('🚨 OVERLAP between', sorted[i - 1].sel, 'and', sorted[i].sel, '— gap', gap, 'px');
  }
  await browser.close();
})();
```

## Recipe 3 — log in as admin to test CRM behaviour

Use sparingly — the admin password is sensitive. Always scrub it from logs.

```js
const fs = require('fs');
const { chromium } = require('playwright');
const PASS = fs.readFileSync(process.env.HOME + '/.openclaw/credentials/supabase/admin_password.txt', 'utf8').trim();

(async () => {
  const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
  const page = await (await browser.newContext({ ignoreHTTPSErrors: true })).newPage();
  await page.goto('https://oganimy.co.il/crm', { waitUntil: 'networkidle' });
  await page.locator('input[type="email"]').first().fill('sdsd434@gmail.com');
  await page.locator('input[type="password"]').first().fill(PASS);
  await page.locator('button:has-text("כניסה")').first().click();
  await page.waitForTimeout(3500);

  // Now navigate / inspect as admin. Example: open the "unlinked emails"
  // view and assert the buttons exist.
  await page.locator('.side-link[data-view="my-mailbox"]').first().click();
  await page.waitForTimeout(2000);

  // … your test logic here …

  await browser.close();
})();
```

## Recipe 4 — set a temp password for a customer to log in as them

For verifying portal behaviour for a specific customer. Always scramble the
password back after the test.

```js
const cred = Object.fromEntries(
  fs.readFileSync(process.env.HOME + '/.openclaw/credentials/supabase/credentials.env', 'utf8')
    .split('\n').filter(l => l.includes('='))
    .map(l => { const i = l.indexOf('='); return [l.slice(0, i), l.slice(i + 1)]; })
);

const USER_ID = '...';
const TEMP_PASS = 'temp-' + Date.now();

await fetch(`${cred.SUPABASE_URL}/auth/v1/admin/users/${USER_ID}`, {
  method: 'PUT',
  headers: {
    apikey: cred.SUPABASE_SERVICE_ROLE_KEY,
    Authorization: 'Bearer ' + cred.SUPABASE_SERVICE_ROLE_KEY,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ password: TEMP_PASS }),
});

// ... do test work ...

// IMPORTANT: scramble the password back so the test password isn't usable.
await fetch(`${cred.SUPABASE_URL}/auth/v1/admin/users/${USER_ID}`, {
  method: 'PUT',
  headers: {
    apikey: cred.SUPABASE_SERVICE_ROLE_KEY,
    Authorization: 'Bearer ' + cred.SUPABASE_SERVICE_ROLE_KEY,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ password: 'reset-' + Math.random().toString(36) }),
});
```

(After this, the customer must request a password reset to log in again.)

## Recipe 5 — visual diff with the `image` tool

After taking a screenshot, copy it to a directory the assistant can read
(workspace root) and use the `image` analyze tool:

```bash
cp /tmp/oganim-test/foo.png ~/.openclaw/workspace/foo.png
# Then: tool call → image(path=~/.openclaw/workspace/foo.png, prompt="...")
```

`/tmp/oganim-test/` is outside the assistant's read boundary, so screenshots
must live somewhere under `~/.openclaw/workspace/` to be inspected.

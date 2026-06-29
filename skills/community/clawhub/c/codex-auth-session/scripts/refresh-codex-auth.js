const fs = require('fs');
const path = require('path');
const readline = require('readline');
const { chromium } = require('playwright-core');

const ROOT = process.env.CODEX_AUTH_REFRESH_HOME || path.resolve(__dirname, '..');
const PROFILE_DIR = process.env.CODEX_AUTH_REFRESH_PROFILE || path.join(ROOT, 'browser-profile');
const BACKUP_DIR = process.env.CODEX_AUTH_REFRESH_BACKUP || path.join(ROOT, 'backups');
const LOG_DIR = process.env.CODEX_AUTH_REFRESH_LOG || path.join(ROOT, 'logs');
const AUTH_PATH = process.env.CODEX_AUTH_PATH || path.join(process.env.USERPROFILE || '', '.codex', 'auth.json');
const SESSION_URL = 'https://chatgpt.com/api/auth/session';
const LOGIN_URL = 'https://chatgpt.com/';

const args = new Set(process.argv.slice(2));
const loginMode = args.has('--login');
const headless = loginMode ? false : !args.has('--headed');

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function stamp() {
  const d = new Date();
  const pad = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}-${pad(d.getHours())}${pad(d.getMinutes())}${pad(d.getSeconds())}`;
}

function log(event) {
  ensureDir(LOG_DIR);
  const row = { time: new Date().toISOString(), ...event };
  fs.appendFileSync(path.join(LOG_DIR, 'refresh.log.jsonl'), JSON.stringify(row) + '\n', 'utf8');
  const safe = { ...row };
  delete safe.token;
  console.log(JSON.stringify(safe));
}

function findBrowser() {
  const candidates = [
    process.env.CODEX_AUTH_REFRESH_BROWSER,
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
  ].filter(Boolean);

  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) return candidate;
  }
  throw new Error('No Chrome or Edge executable found. Set CODEX_AUTH_REFRESH_BROWSER to the browser path.');
}

function decodeJwtPayload(token) {
  const parts = String(token || '').split('.');
  if (parts.length < 2) return {};
  const payload = parts[1].replace(/-/g, '+').replace(/_/g, '/');
  const padded = payload + '='.repeat((4 - payload.length % 4) % 4);
  return JSON.parse(Buffer.from(padded, 'base64').toString('utf8'));
}

async function promptEnter(message) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  await new Promise((resolve) => rl.question(message, resolve));
  rl.close();
}

async function readSessionFromPage(page) {
  await page.goto(SESSION_URL, { waitUntil: 'domcontentloaded', timeout: 45000 });
  const text = (await page.locator('body').innerText({ timeout: 15000 })).trim();
  let session;

  try {
    session = JSON.parse(text);
  } catch {
    throw new Error(`Session endpoint did not return JSON. First 120 chars: ${text.slice(0, 120)}`);
  }

  const accessToken = session.accessToken || session.access_token || session?.tokens?.access_token;
  if (!accessToken || typeof accessToken !== 'string') {
    throw new Error('Session JSON does not contain accessToken. Browser profile may not be logged in.');
  }

  const payload = decodeJwtPayload(accessToken);
  return {
    accessToken,
    expires: session.expires || null,
    accountId: payload.chatgpt_account_id || payload.account_id || payload.sub || '',
    jwtExp: payload.exp ? new Date(payload.exp * 1000).toISOString() : null,
    userEmail: session?.user?.email || payload.email || ''
  };
}

function readExistingAuth() {
  if (!fs.existsSync(AUTH_PATH)) {
    return {
      auth_mode: 'chatgpt',
      tokens: {
        id_token: '',
        access_token: '',
        refresh_token: '',
        account_id: ''
      }
    };
  }
  return JSON.parse(fs.readFileSync(AUTH_PATH, 'utf8'));
}

function writeAuth(session) {
  ensureDir(path.dirname(AUTH_PATH));
  ensureDir(BACKUP_DIR);

  if (fs.existsSync(AUTH_PATH)) {
    fs.copyFileSync(AUTH_PATH, path.join(BACKUP_DIR, `auth-before-refresh-${stamp()}.json`));
  }

  const auth = readExistingAuth();
  auth.auth_mode = 'chatgpt';
  auth.tokens = auth.tokens || {};
  auth.tokens.id_token = session.accessToken;
  auth.tokens.access_token = session.accessToken;
  auth.tokens.refresh_token = auth.tokens.refresh_token || '';
  auth.tokens.account_id = session.accountId || auth.tokens.account_id || '';
  auth.last_refresh = new Date().toISOString();

  fs.writeFileSync(AUTH_PATH, JSON.stringify(auth, null, 2), { encoding: 'utf8' });
}

async function main() {
  ensureDir(ROOT);
  ensureDir(PROFILE_DIR);
  ensureDir(BACKUP_DIR);
  ensureDir(LOG_DIR);

  const executablePath = findBrowser();
  log({ status: 'starting', mode: loginMode ? 'login' : 'refresh', authPath: AUTH_PATH, profileDir: PROFILE_DIR, browser: executablePath });

  const context = await chromium.launchPersistentContext(PROFILE_DIR, {
    executablePath,
    headless,
    viewport: { width: 1280, height: 860 },
    args: ['--disable-blink-features=AutomationControlled']
  });

  try {
    const page = context.pages()[0] || await context.newPage();

    if (loginMode) {
      await page.goto(LOGIN_URL, { waitUntil: 'domcontentloaded', timeout: 45000 });
      console.log('\nA browser window opened with this project profile.');
      console.log('Log in to ChatGPT there. When ChatGPT is fully loaded, return here and press Enter.\n');
      await promptEnter('Press Enter after login succeeds...');
    }

    const session = await readSessionFromPage(page);
    writeAuth(session);
    log({
      status: 'success',
      accountId: session.accountId ? '[present]' : '[missing]',
      userEmail: session.userEmail ? '[present]' : '[missing]',
      sessionExpires: session.expires,
      jwtExp: session.jwtExp
    });
  } finally {
    await context.close();
  }
}

main().catch((err) => {
  log({ status: 'error', message: String(err.message || err).slice(0, 1000) });
  process.exitCode = 1;
});

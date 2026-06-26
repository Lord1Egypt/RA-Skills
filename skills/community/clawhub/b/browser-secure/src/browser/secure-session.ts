import { chromium, Browser, BrowserContext, Page } from 'playwright';
import { v4 as uuidv4 } from 'uuid';
import fs from 'fs';
import path from 'path';
import os from 'os';
import { execSync } from 'child_process';
import { loadConfig, expandPath, getSitePolicy, getSessionConfig } from '../config/loader.js';
import { getSiteCredentials, extractDomain, interactiveCredentialDiscovery, VaultCredentials } from '../vault/index.js';
import {
  startAuditSession,
  logAction,
  finalizeAuditSession
} from '../security/audit.js';
import {
  requestApproval,
  getActionTier,
  closeApprover,
  UnattendedOptions,
  getCachedCredentials,
  cacheCredentials,
  isCacheValid
} from '../security/approval.js';
import { validateUrl } from '../security/network.js';
import { ChromeProfile } from './chrome-profiles.js';
import {
  copyChromeProfileToTemp
} from './chrome-lifecycle.js';
import {
  startDaemon,
  stopDaemon,
  isDaemonRunning,
  getDaemonStatus,
  loadDaemonState,
  DaemonState
} from './daemon.js';
import {
  logNavigationError,
  logSessionError
} from '../utils/error-log.js';

// Detect system Chrome path
function getChromePath(): string | undefined {
  const platform = os.platform();

  if (platform === 'darwin') {
    // macOS
    const macPath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
    if (fs.existsSync(macPath)) {
      return macPath;
    }
  } else if (platform === 'linux') {
    // Linux - try common paths
    const linuxPaths = [
      '/usr/bin/google-chrome',
      '/usr/bin/google-chrome-stable',
      '/usr/bin/chrome',
      '/snap/bin/chrome',
    ];
    for (const p of linuxPaths) {
      if (fs.existsSync(p)) {
        return p;
      }
    }
    // Try which command
    try {
      return execSync('which google-chrome', { encoding: 'utf-8' }).trim();
    } catch {
      try {
        return execSync('which chromium', { encoding: 'utf-8' }).trim();
      } catch {
        // Fall through to undefined
      }
    }
  } else if (platform === 'win32') {
    // Windows
    const winPaths = [
      'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
      'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
      `${process.env.LOCALAPPDATA}\\Google\\Chrome\\Application\\chrome.exe`,
    ];
    for (const p of winPaths) {
      if (p && fs.existsSync(p)) {
        return p;
      }
    }
  }

  return undefined;
}

let browser: Browser | null = null;
// When --profile is used we launch via launchPersistentContext, which returns
// a BrowserContext directly rather than a Browser. Close via context.close().
let persistentContext: BrowserContext | null = null;
let page: Page | null = null;
let actionCounter = 0;

// Daemon mode: browser persists across tasks
let daemonState: DaemonState | null = null;
let daemonBrowser: Browser | null = null;  // separate from `browser` (non-daemon)
let daemonContext: BrowserContext | null = null;

// Temp copy of the real Chrome profile so we don't conflict with the user's
// running Chrome. Cleaned up in closeBrowser().
let tempProfileDir: string | null = null;

interface SecureSession {
  id: string;
  workDir: string;
  screenshotDir: string;
  startTime: number;
  maxDuration: number;
  site?: string;
  warningShown: boolean;
  suspended: boolean;
  suspendedAt?: number;
  credentialSource?: 'env' | 'vault' | 'cache';
}

let activeSession: SecureSession | null = null;
let timeoutInterval: NodeJS.Timeout | null = null;

interface BrowserOptions {
  site?: string;
  autoVault?: boolean;
  headless?: boolean;
  timeout?: number;
  profile?: ChromeProfile;
  unattended?: UnattendedOptions;
  // When --profile is set and Chrome is running, allow browser-secure to
  // quit Chrome gracefully. In unattended mode this is required.
  closeChrome?: boolean;
}

// Check if vault is locked/unavailable
async function checkVaultLock(): Promise<{ locked: boolean; provider?: string; error?: string }> {
  const config = loadConfig();
  const provider = config.vault.provider;

  try {
    if (provider === '1password') {
      // Check if 1Password CLI is locked
      try {
        execSync('op vault list', { stdio: 'ignore' });
        return { locked: false, provider };
      } catch {
        return { locked: true, provider, error: '1Password vault is locked. Please unlock with "op signin".' };
      }
    } else if (provider === 'bitwarden') {
      // Check if Bitwarden is locked
      try {
        execSync('bw status', { stdio: 'pipe' });
        return { locked: false, provider };
      } catch {
        return { locked: true, provider, error: 'Bitwarden vault is locked. Please unlock with "bw unlock".' };
      }
    } else if (provider === 'keychain') {
      // Keychain doesn't have a lock state we can easily check
      return { locked: false, provider };
    } else if (provider === 'env') {
      return { locked: false, provider };
    }

    return { locked: false, provider };
  } catch (e) {
    return { locked: true, provider, error: `Failed to check vault status: ${e}` };
  }
}

async function promptVaultUnlock(provider: string): Promise<boolean> {
  console.log(`\n🔐 ${provider} vault is locked.`);
  console.log('Please unlock your vault in another terminal, then press Enter to continue...');

  return new Promise((resolve) => {
    const rl = require('readline').createInterface({
      input: process.stdin,
      output: process.stdout
    });

    rl.question('', async () => {
      rl.close();
      // Re-check vault status
      const status = await checkVaultLock();
      resolve(!status.locked);
    });
  });
}

export async function startBrowser(url: string, options: BrowserOptions = {}): Promise<void> {
  // Check for concurrent session
  if (activeSession) {
    throw new Error('Another session is already active. Close it first with: browser-secure close');
  }

  // Validate URL against network policy
  const validation = validateUrl(url);
  if (!validation.valid) {
    throw new Error(`URL blocked: ${validation.error}`);
  }

  // Check vault lock status (unless using env credentials)
  if (!options.unattended?.enabled || options.unattended.credentialSource !== 'env') {
    const vaultStatus = await checkVaultLock();
    if (vaultStatus.locked) {
      if (options.unattended?.enabled) {
        throw new Error(`Vault is locked in unattended mode: ${vaultStatus.error}`);
      }
      const unlocked = await promptVaultUnlock(vaultStatus.provider || 'Vault');
      if (!unlocked) {
        throw new Error('Vault remained locked. Cannot proceed.');
      }
    }
  }

  // Start audit session
  const sessionId = startAuditSession(options.site);
  console.log(`🔒 Secure session started: ${sessionId}`);

  // Create isolated session
  activeSession = createSecureSession(options.site, options.timeout, options.unattended?.credentialSource);
  console.log(`📁 Work directory: ${activeSession.workDir}`);

  // Setup timeout watcher
  setupTimeoutWatcher(async () => {
    await closeBrowser();
  });

  // Initialize Playwright with security settings
  const config = loadConfig();
  const chromePath = getChromePath();

  if (chromePath) {
    console.log(`🌐 Using system Chrome: ${chromePath}`);
  } else {
    console.log('⚠️  System Chrome not found, using bundled Chromium (extensions unavailable)');
  }

  // ─── DAEMON MODE ───────────────────────────────────────────────────────────
  // If a daemon is already running for this profile, connect to it and open a new tab.
  // Otherwise, fall back to the existing launch logic (non-daemon, closed after each task).
  const useProfile = !!options.profile;

  if (useProfile) {
    const existingDaemon = loadDaemonState();

    if (existingDaemon && isDaemonRunning(existingDaemon) && existingDaemon.profileId === options.profile!.id) {
      // Same profile daemon: connect and open a new tab
      console.log(`🔁 Reusing existing daemon for profile: ${existingDaemon.profile} [${existingDaemon.profileId}]`);
      daemonState = existingDaemon;
      daemonBrowser = await chromium.connectOverCDP(existingDaemon.wsUrl);

      // When connecting to an existing Chrome via CDP, newContext() is not
      // supported (Chrome only has its default persistent context). Re-use it.
      daemonContext = daemonBrowser.contexts()[0] ?? null;
      if (!daemonContext) {
        throw new Error('Connected to daemon but no default browser context found');
      }
      page = await daemonContext.newPage();
      console.log(`✅ Opened new tab in daemon (profile: ${daemonState.profile} [${daemonState.profileId}])`);

    } else {
      // No daemon for this profile (or daemon stale) — copy the real profile
      // to a temp dir and launch against that copy. This avoids SingletonLock
      // conflicts with the user's running Chrome.
      const prof = options.profile!;
      console.log(`🔐 Using Chrome profile: ${prof.name} [${prof.id}]`);

      tempProfileDir = copyChromeProfileToTemp(prof.id);
      const profileArgs = prof.id === 'Default' ? [] : [`--profile-directory=${prof.id}`];

      persistentContext = await chromium.launchPersistentContext(tempProfileDir, {
        headless: options.headless ?? false,
        executablePath: chromePath || undefined,
        args: [
          ...profileArgs,
          '--disable-gpu',
          '--disable-dev-shm-usage',
          '--disable-software-rasterizer',
          '--disable-webgl',
          '--disable-accelerated-2d-canvas',
        ],
      });

      // Persistent contexts open with one blank page already; reuse it.
      page = persistentContext.pages()[0] ?? await persistentContext.newPage();
    }
  } else {
    // No profile: use Playwright's bundled Chromium (isolated, no cookies from system Chrome)
    // No executablePath → Playwright uses its bundled browser
    browser = await chromium.launch({
      headless: options.headless ?? false,
    });
    const context = await browser.newContext();
    page = await context.newPage();
    console.log(`🔓 Using Playwright Chromium (bundled, isolated/incognito)`);
  }

  // Navigate to URL
  logAction('navigate', { url });

  // Handle welcome page (file:// protocol is blocked by Playwright, use setContent instead)
  if (url.startsWith('file://') && url.includes('welcome.html')) {
    const welcomePath = url.replace('file://', '');
    try {
      const welcomeHtml = fs.readFileSync(welcomePath, 'utf-8');
      await page.setContent(welcomeHtml, { waitUntil: 'networkidle' });
      console.log('✅ Opened welcome page');
    } catch (e) {
      throw new Error(`Failed to load welcome page: ${e}`);
    }
  } else {
    try {
      await page.goto(url);
      console.log(`✅ Navigated to ${url}`);
    } catch (e) {
      const err = e instanceof Error ? e : new Error(String(e));
      logNavigationError(url, `Navigation failed: ${err.message}`, err);
      throw e;
    }
  }

  // Handle site authentication if specified or auto-vault is enabled
  if (options.site) {
    await handleSiteAuthentication(options.site, options.unattended);
  } else if (options.autoVault) {
    await handleAutoVaultAuthentication(url, options.unattended);
  }

  // Take initial screenshot
  await takeScreenshot('navigate');
}

function createSecureSession(site?: string, maxDurationMs?: number, credentialSource?: 'env' | 'vault' | 'cache'): SecureSession {
  const config = loadConfig();
  const sessionConfig = getSessionConfig();
  const id = `bs-${Date.now()}-${uuidv4().slice(0, 8)}`;

  const workDir = path.join(os.tmpdir(), `browser-secure-${id}`);
  const screenshotDir = path.join(workDir, 'screenshots');

  // Create isolated work directory
  if (config.isolation.secureWorkdir) {
    fs.mkdirSync(screenshotDir, { recursive: true });
  }

  // Use session TTL from config (30 min default) or site-specific override
  let sessionTtlMs = maxDurationMs || sessionConfig.ttlMinutes * 60 * 1000;
  if (site) {
    const sitePolicy = getSitePolicy(site);
    if (sitePolicy?.sessionTtlMinutes) {
      sessionTtlMs = sitePolicy.sessionTtlMinutes * 60 * 1000;
    }
  }

  return {
    id,
    workDir,
    screenshotDir,
    startTime: Date.now(),
    maxDuration: sessionTtlMs,
    site,
    warningShown: false,
    suspended: false,
    credentialSource
  };
}

function setupTimeoutWatcher(onTimeout: () => void): void {
  if (!activeSession) return;

  const sessionConfig = getSessionConfig();
  const warningAtMs = sessionConfig.warningAtMinutes * 60 * 1000;

  timeoutInterval = setInterval(() => {
    if (!activeSession) {
      if (timeoutInterval) clearInterval(timeoutInterval);
      return;
    }

    // Don't count time while suspended
    if (activeSession.suspended) {
      return;
    }

    const elapsed = Date.now() - activeSession.startTime;

    // Show warning before timeout
    if (!activeSession.warningShown && elapsed > warningAtMs && elapsed < activeSession.maxDuration) {
      const remaining = Math.floor((activeSession.maxDuration - elapsed) / 1000);
      console.log(`\n⚠️  Session warning: ${remaining}s remaining until timeout`);
      activeSession.warningShown = true;
    }

    if (elapsed > activeSession.maxDuration) {
      if (timeoutInterval) clearInterval(timeoutInterval);
      console.log('\n⚠️  Session timed out. Closing browser...');
      onTimeout();
    }
  }, 5000);
}

export async function handleSiteAuthentication(site: string, unattended?: UnattendedOptions): Promise<void> {
  if (!page) return;

  // Check credential cache first
  let creds: VaultCredentials | null = null;
  let fromCache = false;

  if (unattended?.credentialSource === 'cache' || !unattended?.credentialSource) {
    if (isCacheValid(site)) {
      creds = await getCachedCredentials(site);
      if (creds) {
        console.log(`🔐 Using cached credentials for ${site}`);
        fromCache = true;
      }
    }
  }

  // Request approval for authentication
  const approval = await requestApproval({
    action: 'authenticate',
    site,
    tier: 'authentication'
  }, { unattended });

  if (!approval.approved) {
    throw new Error('Authentication not approved by user');
  }

  logAction('authentication_request', { site, approved: true }, {
    userApproved: true,
    approvalToken: approval.token
  });

  // Get credentials from vault if not cached
  if (!creds) {
    console.log(`🔐 Retrieving credentials for ${site}...`);

    if (unattended?.credentialSource === 'env') {
      // Use environment credentials
      const prefix = `BROWSER_SECURE_${site.toUpperCase()}`;
      creds = {
        username: process.env[`${prefix}_USERNAME`],
        password: process.env[`${prefix}_PASSWORD`],
        token: process.env[`${prefix}_TOKEN`]
      };
      if (!creds.username && !creds.token) {
        throw new Error(`No environment credentials found for ${site}`);
      }
    } else {
      creds = await getSiteCredentials(site);
    }

    // Cache credentials for future use
    if (creds && (creds.username || creds.password || creds.token)) {
      await cacheCredentials(site, creds);
    }
  }

  // Find and fill login form
  if (creds.username && creds.password) {
    await fillLoginForm(creds.username, creds.password);
  } else if (creds.token) {
    console.log('Token-based authentication available');
  }
}

async function handleAutoVaultAuthentication(url: string, unattended?: UnattendedOptions): Promise<void> {
  if (!page) return;

  const domain = extractDomain(url);
  console.log(`🔍 Auto-discovering credentials for ${domain}...`);

  // Use interactive discovery (not available in unattended mode)
  if (unattended?.enabled) {
    console.log('⏭️  Auto-vault discovery skipped in unattended mode.');
    return;
  }

  const discovery = await interactiveCredentialDiscovery(url, domain);

  if (!discovery || !discovery.credentials) {
    console.log('⏭️  No credentials selected. Continuing without authentication.');
    return;
  }

  const { credentials, siteKey } = discovery;

  // Request approval for authentication
  const approval = await requestApproval({
    action: 'authenticate',
    site: siteKey,
    tier: 'authentication'
  }, { unattended });

  if (!approval.approved) {
    throw new Error('Authentication not approved by user');
  }

  logAction('authentication_request', { site: siteKey, approved: true, method: 'auto_vault' }, {
    userApproved: true,
    approvalToken: approval.token
  });

  // Find and fill login form
  if (credentials.username && credentials.password) {
    await fillLoginForm(credentials.username, credentials.password);
  } else if (credentials.token) {
    console.log('Token-based authentication available');
  }
}

async function fillLoginForm(username: string, password: string): Promise<void> {
  if (!page) return;

  try {
    // Look for common username/email fields
    const usernameSelectors = [
      'input[type="email"]',
      'input[name="email"]',
      'input[name="username"]',
      'input[id="username"]',
      'input[id="login"]',
      'input[name="login"]'
    ];

    for (const selector of usernameSelectors) {
      const field = await page.$(selector);
      if (field) {
        await field.fill(username);
        break;
      }
    }

    // Fill password
    const passwordInput = await page.$('input[type="password"]');
    if (passwordInput) {
      await passwordInput.fill(password);
      logAction('fill_password', { method: 'vault_injected' }, { userApproved: true });
    }

    await takeScreenshot('login');
  } catch (e) {
    throw new Error(`Failed to fill login form: ${e}`);
  }
}

export async function performAction(action: string, options?: { autoApprove?: boolean; unattended?: UnattendedOptions }): Promise<void> {
  if (!page || !(browser || persistentContext || daemonBrowser)) {
    throw new Error('Browser not started. Call navigate first.');
  }

  if (isSessionExpired()) {
    throw new Error('Session has expired. Please start a new session.');
  }

  if (activeSession?.suspended) {
    throw new Error('Session is suspended. Use resume command to continue.');
  }

  // Determine action tier and get approval
  const tier = getActionTier(action.split(' ')[0]);

  if (tier !== 'read_only') {
    const approval = await requestApproval({
      action,
      tier
    }, { autoApprove: options?.autoApprove, unattended: options?.unattended });

    if (!approval.approved) {
      throw new Error(`Action "${action}" not approved`);
    }
  }

  // Simple action parsing (click, type, select)
  const lowerAction = action.toLowerCase();

  if (lowerAction.includes('click')) {
    // Extract what to click
    const match = action.match(/click\s+(?:the\s+)?(.+)/i);
    if (match) {
      const target = match[1].trim();
      await performClick(target);
    }
  } else if (lowerAction.includes('type') || lowerAction.includes('fill')) {
    // Extract field and value
    const match = action.match(/(?:type|fill)\s+(.+?)\s+(?:in(?:to)?|with)\s+(.+)/i);
    if (match) {
      const value = match[1].trim();
      const field = match[2].trim();
      await performType(field, value);
    }
  } else if (lowerAction.includes('select')) {
    const match = action.match(/select\s+(.+?)\s+from\s+(.+)/i);
    if (match) {
      const value = match[1].trim();
      const field = match[2].trim();
      await performSelect(field, value);
    }
  } else if (lowerAction.includes('press') || lowerAction.includes('hit')) {
    const match = action.match(/(?:press|hit)\s+(?:the\s+)?(?:key\s+)?(.+)/i);
    if (match) {
      const key = match[1].trim();
      await performPress(key);
    }
  }

  logAction('act', { instruction: action });
  actionCounter++;
  await takeScreenshot(action);
}

async function performClick(target: string): Promise<void> {
  if (!page) return;

  // Try various selectors
  const selectors = [
    `text="${target}"`,
    `button:has-text("${target}")`,
    `a:has-text("${target}")`,
    `[aria-label*="${target}"]`,
    `[title*="${target}"]`,
    `#${target}`,
    `.${target}`
  ];

  for (const selector of selectors) {
    try {
      await page.click(selector, { timeout: 1000 });
      return;
    } catch {
      continue;
    }
  }

  throw new Error(`Could not find element to click: ${target}`);
}

async function performType(field: string, value: string): Promise<void> {
  if (!page) return;

  const selectors = [
    `input[placeholder*="${field}"]`,
    `input[name*="${field}"]`,
    `input[id*="${field}"]`,
    `textarea[placeholder*="${field}"]`,
    `label:has-text("${field}") + input`
  ];

  for (const selector of selectors) {
    try {
      await page.fill(selector, value, { timeout: 1000 });
      return;
    } catch {
      continue;
    }
  }

  throw new Error(`Could not find field: ${field}`);
}

async function performSelect(field: string, value: string): Promise<void> {
  if (!page) return;

  const selectors = [
    `select[name*="${field}"]`,
    `select[id*="${field}"]`,
    `label:has-text("${field}") + select`
  ];

  for (const selector of selectors) {
    try {
      await page.selectOption(selector, { label: value }, { timeout: 1000 });
      return;
    } catch {
      try {
        await page.selectOption(selector, { value }, { timeout: 1000 });
        return;
      } catch {
        continue;
      }
    }
  }

  throw new Error(`Could not select ${value} from ${field}`);
}

async function performPress(key: string): Promise<void> {
  if (!page) return;

  const keyMap: Record<string, string> = {
    'enter': 'Enter',
    'return': 'Enter',
    'esc': 'Escape',
    'escape': 'Escape',
    'tab': 'Tab',
    'space': 'Space',
    'backspace': 'Backspace',
    'delete': 'Delete',
    'arrowup': 'ArrowUp',
    'up': 'ArrowUp',
    'arrowdown': 'ArrowDown',
    'down': 'ArrowDown',
    'arrowleft': 'ArrowLeft',
    'left': 'ArrowLeft',
    'arrowright': 'ArrowRight',
    'right': 'ArrowRight',
  };

  const normalized = keyMap[key.toLowerCase()] || key;
  await page.keyboard.press(normalized);
}

export async function extractData(instruction: string, schema?: Record<string, unknown>): Promise<unknown> {
  if (!page) {
    throw new Error('Browser not started. Call navigate first.');
  }

  if (isSessionExpired()) {
    throw new Error('Session has expired. Please start a new session.');
  }

  if (activeSession?.suspended) {
    throw new Error('Session is suspended. Use resume command to continue.');
  }

  logAction('extract', { instruction, schema });

  // Simple extraction based on instruction keywords
  const lower = instruction.toLowerCase();

  if (lower.includes('title')) {
    const title = await page.title();
    return { title };
  }

  if (lower.includes('url')) {
    return { url: page.url() };
  }

  if (lower.includes('text') || lower.includes('content')) {
    const text = await page.evaluate(() => document.body?.textContent || '');
    return { text: text.slice(0, 5000) };
  }

  if (lower.includes('links')) {
    const links = await page.$$eval('a', as => as.map(a => ({ text: (a as HTMLElement).innerText, href: (a as HTMLAnchorElement).href })));
    return { links: links.slice(0, 50) };
  }

  if (lower.includes('headlines') || lower.includes('headings')) {
    const headlines = await page.$$eval('h1, h2, h3', hs => hs.map(h => ({ level: h.tagName, text: (h as HTMLElement).innerText })));
    return { headlines };
  }

  // Default: return page info
  return {
    url: page.url(),
    title: await page.title()
  };
}

export function getPage(): Page | null {
  return page;
}

export async function reconnectToDaemon(): Promise<void> {
  const state = loadDaemonState();
  if (!state || !isDaemonRunning(state)) {
    throw new Error('No daemon running. Start one with: browser-secure daemon start --profile <profile>');
  }

  daemonState = state;
  daemonBrowser = await chromium.connectOverCDP(state.wsUrl);
  daemonContext = daemonBrowser.contexts()[0] ?? null;
  if (!daemonContext) {
    throw new Error('Connected to daemon but no default browser context found');
  }

  // Find the most recently active web page (ignore extension/service-worker pages).
  const pages = daemonContext.pages().filter(p => {
    const url = p.url();
    return url.startsWith('http://') || url.startsWith('https://') || url === 'about:blank';
  });
  if (pages.length > 0) {
    page = pages[pages.length - 1];
  } else {
    page = await daemonContext.newPage();
  }

  // Create minimal session for audit/screenshot support
  if (!activeSession) {
    activeSession = createSecureSession(undefined, undefined, undefined);
    const config = loadConfig();
    if (config.isolation.secureWorkdir) {
      fs.mkdirSync(activeSession.screenshotDir, { recursive: true });
    }
  }

  // Start audit session for this command
  startAuditSession();
}

export async function takeScreenshot(action?: string): Promise<string | null> {
  if (!page) return null;

  const config = loadConfig();
  if (!config.security.screenshotEveryAction && action !== 'manual') return null;

  let screenshotDir: string;
  let filename: string;

  if (activeSession) {
    const paddedIndex = String(actionCounter).padStart(3, '0');
    const safeAction = (action || 'screenshot').replace(/[^a-z0-9]/gi, '_').slice(0, 30);
    screenshotDir = activeSession.screenshotDir;
    filename = path.join(screenshotDir, `${activeSession.id}-${paddedIndex}-${safeAction}.png`);
  } else {
    const safeAction = (action || 'screenshot').replace(/[^a-z0-9]/gi, '_').slice(0, 30);
    screenshotDir = os.tmpdir();
    filename = path.join(screenshotDir, `browser-secure-manual-${Date.now()}-${safeAction}.png`);
  }

  try {
    await page.screenshot({ path: filename, fullPage: false });
    logAction('screenshot', { path: filename });
    return filename;
  } catch (e) {
    console.error(`Screenshot failed: ${e}`);
    return null;
  }
}

export async function closeBrowser(options?: { keepPage?: boolean }): Promise<void> {
  const startTime = activeSession?.startTime || Date.now();

  if (timeoutInterval) {
    clearInterval(timeoutInterval);
    timeoutInterval = null;
  }

  closeApprover();

  if (daemonState) {
    // Daemon mode: disconnect from browser. Optionally keep the page open in
    // Chrome so subsequent CLI commands can reconnect and find it.
    if (page && !options?.keepPage) {
      try { await page.close(); } catch { /* */ }
    }
    if (daemonBrowser) {
      try { await daemonBrowser.close(); } catch { /* */ }
    }
    page = null;
    daemonContext = null;
    daemonBrowser = null;
    const msg = options?.keepPage ? 'Disconnected' : 'Tab closed';
    console.log(`🔒 ${msg} (daemon running: ${daemonState.profile} [${daemonState.profileId}])`);
    console.log(`   To stop daemon: browser-secure daemon stop`);
  } else {
    // Non-daemon: close the persistent context (if any) or the browser.
    if (persistentContext) {
      try {
        await persistentContext.close();
      } catch (e) {
        console.error(`Error closing persistent context: ${e}`);
      }
      persistentContext = null;
      page = null;
    }
    if (browser) {
      try {
        await browser.close();
      } catch (e) {
        console.error(`Error closing browser: ${e}`);
      }
      browser = null;
      page = null;
    }
    // Clean up the temp profile copy
    if (tempProfileDir) {
      try {
        fs.rmSync(tempProfileDir, { recursive: true, force: true });
      } catch (e) {
        console.error(`Warning: failed to clean up temp profile dir: ${e}`);
      }
      tempProfileDir = null;
    }
  }

  // Only clean up if we're fully closing (not just disconnecting for next command)
  if (!options?.keepPage) {
    // Secure cleanup (work dir, screenshots)
    const cleanupSuccess = secureCleanup();

    // Finalize audit
    const duration = Math.floor((Date.now() - startTime) / 1000);
    finalizeAuditSession(duration, cleanupSuccess);

    actionCounter = 0;
  }
}

function secureCleanup(): boolean {
  if (!activeSession) return true;

  const config = loadConfig();
  let success = true;

  if (config.isolation.autoCleanup && config.isolation.secureWorkdir) {
    try {
      // Best effort cleanup
      fs.rmSync(activeSession.workDir, { recursive: true, force: true });
    } catch (e) {
      console.error(`Cleanup warning: ${e}`);
      success = false;
    }
  }

  activeSession = null;
  return success;
}

function isSessionExpired(): boolean {
  if (!activeSession) return true;

  // Don't expire while suspended
  if (activeSession.suspended) return false;

  const elapsed = Date.now() - activeSession.startTime;
  return elapsed > activeSession.maxDuration;
}

export function getBrowserStatus(): {
  active: boolean;
  sessionId?: string;
  timeRemaining?: number;
  site?: string;
  actionCount: number;
  suspended?: boolean;
  warningShown?: boolean;
  daemon?: {
    profile: string;
    profileId: string;
    pid: number;
    port: number;
    uptime: string;
  };
} {
  const daemon = daemonState
    ? {
        profile: daemonState.profile,
        profileId: daemonState.profileId,
        pid: daemonState.pid,
        port: daemonState.port,
        uptime: (() => {
          const s = Math.floor((Date.now() - new Date(daemonState!.startedAt).getTime()) / 1000);
          return `${Math.floor(s / 60)}m ${s % 60}s`;
        })()
      }
    : undefined;

  return {
    active: !!browser || !!daemonBrowser,
    sessionId: activeSession?.id,
    timeRemaining: activeSession ? Math.floor((activeSession.maxDuration - (Date.now() - activeSession.startTime)) / 1000) : undefined,
    site: activeSession?.site,
    actionCount: actionCounter,
    suspended: activeSession?.suspended,
    warningShown: activeSession?.warningShown,
    daemon
  };
}

// Suspend the session (pause timeout)
export function suspendSession(): void {
  if (!activeSession) {
    throw new Error('No active session to suspend');
  }
  if (activeSession.suspended) {
    console.log('Session is already suspended');
    return;
  }

  activeSession.suspended = true;
  activeSession.suspendedAt = Date.now();
  console.log('⏸️  Session suspended. Timeout is paused.');
}

// Resume the session (continue timeout)
export function resumeSession(): void {
  if (!activeSession) {
    throw new Error('No active session to resume');
  }
  if (!activeSession.suspended) {
    console.log('Session is already active');
    return;
  }

  // Adjust start time to account for suspension period
  if (activeSession.suspendedAt) {
    const suspendedDuration = Date.now() - activeSession.suspendedAt;
    activeSession.startTime += suspendedDuration;
  }

  activeSession.suspended = false;
  activeSession.suspendedAt = undefined;
  activeSession.warningShown = false; // Reset warning so it shows again
  console.log('▶️  Session resumed. Timeout continues.');
}

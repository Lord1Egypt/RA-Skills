import fs from 'fs';
import path from 'path';
import os from 'os';
import { fileURLToPath } from 'url';
import playwrightPkg from 'playwright';

const { chromium } = playwrightPkg;

export const __dirname = path.dirname(fileURLToPath(import.meta.url));
export const SKILL_ROOT = path.resolve(__dirname, '..');
export const ENDPOINT_FILE = path.join(SKILL_ROOT, '.browser-endpoint');
export const BROWSER_ARGS = [
  '--no-sandbox',
  '--disable-setuid-sandbox',
  '--disable-dev-shm-usage',
];

export function readDaemonInfo() {
  try {
    return JSON.parse(fs.readFileSync(ENDPOINT_FILE, 'utf-8'));
  } catch {
    return null;
  }
}

export function isPidAlive(pid) {
  if (!pid) return false;
  try {
    process.kill(pid, 0);
    return true;
  } catch {
    return false;
  }
}

export function daemonAlive() {
  const info = readDaemonInfo();
  if (!info) return false;
  if (!isPidAlive(info.pid)) {
    try { fs.unlinkSync(ENDPOINT_FILE); } catch {}
    return false;
  }
  return true;
}

function walkExecutable(dir, names) {
  if (!dir || !fs.existsSync(dir)) return null;
  try {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const name of names) {
      const exact = path.join(dir, name);
      if (fs.existsSync(exact)) return exact;
    }
    for (const entry of entries) {
      if (!entry.isDirectory()) continue;
      const child = walkExecutable(path.join(dir, entry.name), names);
      if (child) return child;
    }
  } catch {}
  return null;
}

export function findBrowserExecutable() {
  const envPath = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH || process.env.CHROMIUM_EXECUTABLE_PATH;
  if (envPath && fs.existsSync(envPath)) return envPath;

  const candidateDirs = [
    process.env.PLAYWRIGHT_BROWSERS_PATH,
    path.join(os.homedir(), '.cache', 'ms-playwright'),
    path.join(os.homedir(), 'Library', 'Caches', 'ms-playwright'),
    process.env.LOCALAPPDATA && path.join(process.env.LOCALAPPDATA, 'ms-playwright'),
  ].filter(Boolean);

  const names = [
    'chrome-linux64/chrome',
    'chrome-linux/chrome',
    'chrome-mac/Chromium.app/Contents/MacOS/Chromium',
    'chrome-win/chrome.exe',
    'chrome-headless-shell-linux64/chrome-headless-shell',
    'chrome-headless-shell-linux/chrome-headless-shell',
    'chromium-*/chrome-linux64/chrome',
    'chromium-*/chrome-linux/chrome',
    'chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell',
    'chromium_headless_shell-*/chrome-headless-shell-linux/chrome-headless-shell',
  ];

  for (const base of candidateDirs) {
    if (!fs.existsSync(base)) continue;
    for (const name of names) {
      if (name.includes('*')) {
        const prefix = name.split('*/')[0];
        const suffix = name.split('*/')[1];
        const matches = fs.readdirSync(base, { withFileTypes: true })
          .filter(entry => entry.isDirectory() && entry.name.startsWith(prefix.replace(/\/$/, '')));
        for (const entry of matches) {
          const candidate = path.join(base, entry.name, suffix);
          if (fs.existsSync(candidate)) return candidate;
        }
      } else {
        const candidate = path.join(base, name);
        if (fs.existsSync(candidate)) return candidate;
      }
    }
    const nested = walkExecutable(base, ['chrome', 'chrome.exe', 'chrome-headless-shell']);
    if (nested) return nested;
  }

  try {
    const p = chromium.executablePath();
    if (p && fs.existsSync(p)) return p;
  } catch {}

  return null;
}

export async function launchBrowser(options = {}) {
  const { headless = true, executablePath } = options;
  const execPath = executablePath || findBrowserExecutable();
  return chromium.launch({
    headless,
    executablePath: execPath || undefined,
    args: BROWSER_ARGS,
  });
}

export async function launchBrowserServer(options = {}) {
  const { headless = true, executablePath } = options;
  const execPath = executablePath || findBrowserExecutable();
  return chromium.launchServer({
    headless,
    executablePath: execPath || undefined,
    args: BROWSER_ARGS,
  });
}

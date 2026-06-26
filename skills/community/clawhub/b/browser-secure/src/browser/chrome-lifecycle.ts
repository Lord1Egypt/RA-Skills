import fs from 'fs';
import os from 'os';
import path from 'path';
import readline from 'readline';
import { execFileSync } from 'child_process';

// Returns the platform-specific root directory where Chrome stores all its
// profiles. --profile-directory=<id> names a subfolder inside this dir.
export function getChromeUserDataDir(): string {
  const p = os.platform();
  if (p === 'darwin') {
    return path.join(os.homedir(), 'Library', 'Application Support', 'Google', 'Chrome');
  }
  if (p === 'linux') {
    return path.join(os.homedir(), '.config', 'google-chrome');
  }
  if (p === 'win32') {
    return path.join(os.homedir(), 'AppData', 'Local', 'Google', 'Chrome', 'User Data');
  }
  throw new Error(`Unsupported platform: ${p}`);
}

// Files that should never be copied to a temp profile dir because they
// contain runtime locks, sockets, or machine-specific state.
const EXCLUDED_COPY_FILES = new Set([
  'SingletonLock',
  'SingletonSocket',
  'SingletonCookie',
  'lockfile',
]);

function copyDirSync(src: string, dest: string): void {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    if (EXCLUDED_COPY_FILES.has(entry.name)) continue;
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDirSync(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

/**
 * Copy a Chrome profile from the real user data dir to a temporary directory.
 * This avoids SingletonLock conflicts with the user's running Chrome.
 * The caller is responsible for deleting the temp dir when done.
 */
export function copyChromeProfileToTemp(profileId: string): string {
  const realDir = getChromeUserDataDir();
  const tempDir = path.join(os.tmpdir(), `browser-secure-profile-${Date.now()}`);
  fs.mkdirSync(tempDir, { recursive: true });

  // We intentionally do NOT copy Local State. The real Local State can
  // contain settings/policies that break automation (e.g. CDP's
  // Browser.setDownloadBehavior fails). Chrome creates a fresh one on startup.
  // Create First Run marker so Chrome doesn't show welcome UI.
  fs.writeFileSync(path.join(tempDir, 'First Run'), '');

  // Copy the requested profile directory
  const profileSrc = path.join(realDir, profileId);
  const profileDest = path.join(tempDir, profileId);
  if (fs.existsSync(profileSrc)) {
    copyDirSync(profileSrc, profileDest);
  } else {
    throw new Error(`Profile directory "${profileId}" not found in ${realDir}`);
  }

  // Restrict permissions on the temp copy
  try {
    fs.chmodSync(tempDir, 0o700);
  } catch { /* ignore on platforms where chmod is limited */ }

  return tempDir;
}

// Chrome writes SingletonLock (mac/linux) or SingletonLock-shaped files to its
// user data dir while running. A stale lock can be left behind after a crash
// or force-kill, so we verify there is an actual Chrome process.
export function isChromeRunning(): boolean {
  const p = os.platform();
  if (p === 'win32') {
    // SingletonLock on Windows is inside each profile; just check for any
    // chrome.exe process via tasklist would be more reliable but requires
    // shelling out. For now return false on Windows — users must close
    // Chrome themselves. Documented in SKILL.md.
    return false;
  }

  // Check for actual Chrome processes first
  const names = p === 'darwin'
    ? ['Google Chrome', 'Chromium']
    : ['google-chrome', 'chrome', 'chromium'];
  for (const name of names) {
    try {
      execFileSync('pgrep', ['-x', name], { stdio: 'ignore' });
      return true;
    } catch { /* try next */ }
  }

  // If no process found, a stale lock is not "running"
  const lock = path.join(getChromeUserDataDir(), 'SingletonLock');
  try {
    fs.lstatSync(lock);
    return false;
  } catch {
    return false;
  }
}

async function waitForChromeExit(maxWaitMs = 15000): Promise<boolean> {
  const deadline = Date.now() + maxWaitMs;
  while (Date.now() < deadline) {
    if (!isChromeRunning()) return true;
    await new Promise(r => setTimeout(r, 500));
  }
  return false;
}

async function promptQuit(profileName: string): Promise<boolean> {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const question =
    '\n⚠️  Profile mode requires exclusive access to your Chrome user data dir.\n' +
    `    Chrome will be asked to quit gracefully (session state is saved).\n` +
    `    Profile: ${profileName}\n\n` +
    '    Continue? [y/N]: ';
  const answer = await new Promise<string>(resolve =>
    rl.question(question, ans => resolve(ans.trim()))
  );
  rl.close();
  return /^y(es)?$/i.test(answer);
}

function quitChromeProcess(): void {
  const p = os.platform();
  if (p === 'darwin') {
    // Try targeted pkill first (avoids quitting *all* Chrome windows via AppleScript)
    try {
      execFileSync('pkill', ['-SIGTERM', '-x', 'Google Chrome'], { stdio: 'ignore' });
      return;
    } catch { /* fallback to AppleScript */ }
    execFileSync(
      'osascript',
      ['-e', 'tell application "Google Chrome" to quit'],
      { stdio: 'ignore' }
    );
    return;
  }
  if (p === 'linux') {
    // Graceful SIGTERM to all chrome/google-chrome processes.
    // pkill returns non-zero if no match; swallow and let the poll decide.
    for (const name of ['google-chrome', 'chrome', 'chromium']) {
      try {
        execFileSync('pkill', ['-SIGTERM', name], { stdio: 'ignore' });
      } catch { /* no match is fine */ }
    }
    return;
  }
  throw new Error(
    `Auto-quit for Chrome is not supported on ${p}. Close Chrome manually and retry.`
  );
}

export interface EnsureChromeClosedOptions {
  profileName: string;
  // When true, skip the interactive confirmation (e.g. unattended mode with
  // --close-chrome). Caller is responsible for having asked the user.
  allowQuit: boolean;
  // When true, we are in unattended mode; absent explicit allowQuit we throw
  // instead of silently continuing.
  isUnattended: boolean;
}

export async function ensureChromeClosedForProfile(
  opts: EnsureChromeClosedOptions
): Promise<void> {
  if (!isChromeRunning()) return;

  if (opts.isUnattended && !opts.allowQuit) {
    throw new Error(
      'Chrome is running and --profile requires exclusive access to its user data dir.\n' +
      'In unattended mode, pass --close-chrome to allow browser-secure to quit it for you, ' +
      'or run without --profile to use an isolated Playwright Chromium instance.'
    );
  }

  if (!opts.isUnattended && !opts.allowQuit) {
    const ok = await promptQuit(opts.profileName);
    if (!ok) {
      throw new Error(
        'Aborted: Chrome still running. Retry with Chrome closed, or omit --profile.'
      );
    }
  }

  console.log('🛑 Asking Chrome to quit gracefully...');
  quitChromeProcess();

  const exited = await waitForChromeExit(15000);
  if (!exited) {
    throw new Error(
      'Chrome did not exit within 15s. It may have an unsaved-changes dialog open. ' +
      'Dismiss it and retry.'
    );
  }
  console.log('✅ Chrome closed.');
}

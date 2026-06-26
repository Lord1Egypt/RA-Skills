import { execSync } from 'node:child_process';
import os from 'node:os';
import path from 'node:path';
import process from 'node:process';

const APP_DATA_DIR = 'baoyu-skills';
const FLOW_DATA_DIR = 'flow-web';
const COOKIE_FILE_NAME = 'cookies.json';
const PROFILE_DIR_NAME = 'chrome-profile';
const DEFAULT_WSL_DEBUG_PROFILE = '/mnt/c/chrome-debug-openclaw';

export function resolveUserDataRoot(): string {
  if (process.platform === 'win32') {
    return process.env.APPDATA ?? path.join(os.homedir(), 'AppData', 'Roaming');
  }
  if (process.platform === 'darwin') {
    return path.join(os.homedir(), 'Library', 'Application Support');
  }
  return process.env.XDG_DATA_HOME ?? path.join(os.homedir(), '.local', 'share');
}

export function resolveFlowWebDataDir(): string {
  const override = process.env.FLOW_WEB_DATA_DIR?.trim();
  if (override) return path.resolve(override);
  return path.join(resolveUserDataRoot(), APP_DATA_DIR, FLOW_DATA_DIR);
}

export function resolveFlowWebCookiePath(): string {
  const override = process.env.FLOW_WEB_COOKIE_PATH?.trim();
  if (override) return path.resolve(override);
  return path.join(resolveFlowWebDataDir(), COOKIE_FILE_NAME);
}

function toWslPath(rawWindowsPath: string): string | null {
  try {
    return execSync(`wslpath -u "${rawWindowsPath}"`, { encoding: 'utf-8', timeout: 5000 }).trim() || null;
  } catch {
    return null;
  }
}

/** Default Chrome user data dir used for CDP launches. */
export function resolveFlowWebChromeProfileDir(): string {
  const override = process.env.BAOYU_CHROME_PROFILE_DIR?.trim() || process.env.FLOW_WEB_CHROME_PROFILE_DIR?.trim();
  if (override) return path.resolve(override);
  if (process.env.WSL_DISTRO_NAME) {
    const winOverride = process.env.AGENT_BROWSER_USER_DATA_DIR_WIN?.trim() || process.env.FLOW_WEB_CHROME_USER_DATA_DIR_WIN?.trim();
    if (winOverride) {
      const converted = toWslPath(winOverride);
      if (converted) return converted;
    }
    return DEFAULT_WSL_DEBUG_PROFILE;
  }
  return path.join(resolveUserDataRoot(), APP_DATA_DIR, PROFILE_DIR_NAME);
}

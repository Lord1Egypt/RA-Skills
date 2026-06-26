/**
 * Git operations for backup skill
 */

import { exec } from 'child_process';
import { promisify } from 'util';
import fs from 'fs';
import path from 'path';

const execAsync = promisify(exec);

const DOT = process.env.OPENCLAW_DIR || process.env.HOME + '/.openclaw';

/**
 * Execute git command in openclaw directory
 */
async function git(...args) {
  const cmd = 'git ' + args.join(' ');
  const { stdout } = await execAsync(cmd, { cwd: DOT });
  return stdout.trim();
}

/**
 * Check if directory is a git repo
 */
export async function isGitRepo() {
  try {
    await execAsync(`git rev-parse --git-dir`, { cwd: DOT });
    return true;
  } catch {
    return false;
  }
}

/**
 * Init git repo and add remote
 */
export async function initRepo(repoUrl, token) {
  const remoteUrl = token ? repoUrl.replace('://', `://${token}@`) : repoUrl;

  if (!await isGitRepo()) {
    await execAsync(`git init`, { cwd: DOT });
    await execAsync(`git config user.name "OpenClaw Backup"`, { cwd: DOT });
    await execAsync(`git config user.email "backup@openclaw"`, { cwd: DOT });
    await execAsync(`git config init.defaultBranch main`, { cwd: DOT });
  } else {
    // Ensure remote URL is current (token may have rotated)
    try { await execAsync(`git remote set-url origin ${remoteUrl}`, { cwd: DOT }); } catch { /* ignore */ }
  }

  // Add remote if not exists
  try {
    await execAsync(`git remote add origin ${remoteUrl}`, { cwd: DOT });
  } catch {
    // already exists — ignore
  }

  return true;
}

/**
 * Stage all changes including .gitignore itself
 */
export async function stageAll() {
  await execAsync(`git add -A`, { cwd: DOT });
}

/**
 * Stage RESTORE.md specifically
 */
export async function stageRestoreMd() {
  try {
    await execAsync(`git add RESTORE.md`, { cwd: DOT });
  } catch { /* ignore if file doesn't exist */ }
}

/**
 * Amend the previous commit with staged changes (no new commit).
 * Used to add RESTORE.md to the already-committed backup.
 */
export async function commitAmend(filename) {
  await execAsync(`git commit --amend --no-edit --include "${filename}"`, { cwd: DOT });
}

/**
 * Check if there are uncommitted changes
 */
export async function hasChanges() {
  const { stdout } = await execAsync(`git status --porcelain`, { cwd: DOT });
  return stdout.length > 0;
}

/**
 * Create commit with timestamp
 */
export async function commit() {
  const now = new Date().toISOString().replace('T', ' ').substring(0, 19);
  return await execAsync(`git commit -m "backup: ${now}"`, { cwd: DOT });
}

/**
 * Push with retry and exponential backoff.
 * Stderr is redirected to suppress token-in-URL from error messages.
 */
export async function push(repoUrl, token, retries = 3, retryMs = 60000) {
  const remoteUrl = token
    ? repoUrl.replace('://', `://${token}@`)
    : repoUrl;

  // Update remote with fresh token
  try {
    await execAsync(`git remote set-url origin ${remoteUrl}`, { cwd: DOT });
  } catch { /* ignore */ }

  let lastError;
  for (let i = 0; i < retries; i++) {
    try {
      // 2>/dev/null prevents token from leaking in error output
      await execAsync(`git push -u origin main 2>/dev/null`, { cwd: DOT });
      return true;
    } catch (e) {
      lastError = e;
      if (i < retries - 1) {
        const delay = retryMs * Math.pow(2, i); // 60s → 120s → 240s
        await sleep(delay);
      }
    }
  }
  throw lastError;
}

/**
 * Clone repo to target directory
 */
export async function clone(repoUrl, token, targetDir) {
  const remoteUrl = token ? repoUrl.replace('://', `://${token}@`) : repoUrl;
  await execAsync(`git clone ${remoteUrl} ${targetDir} 2>/dev/null`);
}

/**
 * List recent commits in a repo clone
 */
export async function log(dir, limit = 5) {
  const { stdout } = await execAsync(
    `git log --oneline -${limit}`,
    { cwd: dir }
  );
  return stdout.split('\n').filter(Boolean);
}

/**
 * Checkout specific commit in target dir
 */
export async function checkout(commitHash, targetDir) {
  await execAsync(`git checkout ${commitHash}`, { cwd: targetDir });
}

/**
 * Get current commit hash
 */
export async function currentCommit() {
  try {
    return await git('rev-parse', 'HEAD');
  } catch {
    return null;
  }
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

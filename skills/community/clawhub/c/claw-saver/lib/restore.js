/**
 * Restore logic for backup skill
 */

import { exec } from 'child_process';
import { promisify } from 'util';
import fs from 'fs';
import path from 'path';
import os from 'os';
import readline from 'readline';

import * as git from './git.js';

const execAsync = promisify(exec);

const DOT = process.env.OPENCLAW_DIR || process.env.HOME + '/.openclaw';

/**
 * List available backups (recent commits)
 */
export async function listBackups() {
  const token = process.env.OPENCLAW_BACKUP_GIT_TOKEN;
  const config = await loadConfig();

  const tmpDir = await fs.promises.mkdtemp(path.join(os.tmpdir(), 'backup-list-'));

  try {
    await git.clone(config.repo, token, tmpDir);
    const commits = await git.log(tmpDir, 10);
    return commits;
  } finally {
    await fs.promises.rm(tmpDir, { recursive: true, force: true });
  }
}

/**
 * Restore from a specific commit
 */
export async function restoreBackup(commit, { confirm = false } = {}) {
  const token = process.env.OPENCLAW_BACKUP_GIT_TOKEN;
  const config = await loadConfig();

  // Guard: non-interactive mode requires confirm=true
  if (!confirm) {
    if (!process.stdin.isTTY) {
      console.error('Error: restore requires TTY for interactive confirmation. Use { confirm: true } to bypass.');
      return { cancelled: true, error: 'non-interactive' };
    }
    const warning = `This will overwrite current files with version from ${commit}. Continue? [y/N]`;
    process.stdout.write(warning + ' ');
    const answer = await promptYesNo();
    if (!answer) return { cancelled: true };
    confirm = true;
  }

  const tmpDir = await fs.promises.mkdtemp(path.join(os.tmpdir(), 'backup-restore-'));

  // Preserve paths that must survive the clean
  const preservedBackupDir = path.join(DOT, 'skills/claw-saver');
  let savedBackup = null;

  try {
    await git.clone(config.repo, token, tmpDir);
    await git.checkout(commit, tmpDir);

    // Snapshot the active skill directory before we nuke DOT
    try {
      const stat = await fs.promises.stat(preservedBackupDir);
      if (stat.isDirectory()) {
        savedBackup = await fs.promises.mkdtemp(path.join(os.tmpdir(), 'backup-skill-'));
        await copyRecursive(preservedBackupDir, savedBackup);
      }
    } catch { /* skill dir not present, nothing to save */ }

    // Wipe DOT clean (preserves only .git dir and lock file)
    await cleanDirectory(DOT, ['.git', '.backup.lock']);

    // Restore everything from the backup snapshot
    const files = await fs.promises.readdir(tmpDir);
    for (const file of files) {
      if (file === '.git') continue;
      const src = path.join(tmpDir, file);
      const dest = path.join(DOT, file);
      await copyRecursive(src, dest);
    }

    // Put the live skill back (in case it had uncommitted local changes)
    if (savedBackup) {
      await copyRecursive(savedBackup, preservedBackupDir);
    }

    console.log('Restore complete. Restart OpenClaw Gateway to apply changes.');
    return { success: true, commit };
  } finally {
    if (tmpDir) await fs.promises.rm(tmpDir, { recursive: true, force: true });
    if (savedBackup) await fs.promises.rm(savedBackup, { recursive: true, force: true });
  }
}

/**
 * Prompt user for yes/no (TTY only)
 */
function promptYesNo() {
  if (!process.stdin.isTTY) {
    throw new Error('Interactive restore not supported in non-TTY environment. Use openclaw backup restore with --yes flag or restore from a specific commit directly.');
  }
  return new Promise((resolve) => {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    rl.question('', (answer) => {
      rl.close();
      resolve(answer.toLowerCase() === 'y');
    });
  });
}

/**
 * Copy directory recursively
 */
async function copyRecursive(src, dest) {
  const stat = await fs.promises.stat(src);
  if (stat.isDirectory()) {
    await fs.promises.mkdir(dest, { recursive: true });
    const entries = await fs.promises.readdir(src);
    for (const entry of entries) {
      await copyRecursive(path.join(src, entry), path.join(dest, entry));
    }
  } else {
    await fs.promises.copyFile(src, dest);
  }
}

/**
 * Clean directory but preserve certain entries
 */
async function cleanDirectory(dir, preserve) {
  try {
    const entries = await fs.promises.readdir(dir);
    for (const entry of entries) {
      if (preserve.includes(entry)) continue;
      const full = path.join(dir, entry);
      const stat = await fs.promises.stat(full);
      if (stat.isDirectory()) {
        await fs.promises.rm(full, { recursive: true, force: true });
      } else {
        await fs.promises.unlink(full);
      }
    }
  } catch { /* ignore */ }
}

async function loadConfig() {
  const configPath = path.join(DOT, 'skills/claw-saver/config.json');
  try {
    return JSON.parse(fs.readFileSync(configPath, 'utf8'));
  } catch {
    return {
      repo: 'https://example.com/user/repo',
      push_retries: 3,
      push_retry_interval_ms: 60000,
    };
  }
}
/**
 * Git LFS configuration for backup skill
 */

import { exec } from 'child_process';
import { promisify } from 'util';
import fs from 'fs';
import path from 'path';

const execAsync = promisify(exec);

const DOT = process.env.OPENCLAW_DIR || process.env.HOME + '/.openclaw';

/**
 * LFS extensions to track (files >10MB threshold)
 */
const LFS_EXTENSIONS = [
  '.bin',
  '.gguf',
  '.safetensors',
  '.pt',
  '.pth',
  '.onnx',
  '.msgpack',
  '.model',
];

/**
 * Check if git lfs is installed
 */
export async function isLfsInstalled() {
  try {
    await execAsync(`git lfs version`);
    return true;
  } catch {
    return false;
  }
}

/**
 * Initialize LFS (creates .gitattributes)
 */
export async function lfsInit() {
  // Ensure .gitattributes exists
  const attrsPath = path.join(DOT, '.gitattributes');

  const patterns = LFS_EXTENSIONS.map((ext) => `*${ext} filter=lfs diff=lfs merge=lfs -text`);

  fs.writeFileSync(attrsPath, patterns.join('\n') + '\n');

  // Stage .gitattributes
  await execAsync(`git add .gitattributes`, { cwd: DOT });
}

/**
 * Verify LFS tracked files
 */
export async function lfsVerify() {
  try {
    const { stdout } = await execAsync(`git lfs ls-files`, { cwd: DOT });
    return stdout.split('\n').filter(Boolean);
  } catch {
    return [];
  }
}

/**
 * Get LFS tracked file count and total size
 */
export async function lfsStatus() {
  try {
    const { stdout } = await execAsync(`git lfs status`, { cwd: DOT });
    return stdout.trim();
  } catch {
    return null;
  }
}
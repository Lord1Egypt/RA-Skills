/**
 * Shared .env loader for all buddy scripts.
 *
 * Searches standard locations in order and loads the first .env found.
 * Existing environment variables are never overwritten.
 *
 * Usage:
 *   import { loadEnv } from './lib/env.js';
 *   loadEnv();
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import os from 'os';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const SKILL_DIR = path.resolve(__dirname, '..', '..');

function stripInlineComment(val) {
  let inSingleQuote = false;
  let inDoubleQuote = false;

  for (let i = 0; i < val.length; i++) {
    const ch = val[i];

    if (ch === "'" && !inDoubleQuote) {
      inSingleQuote = !inSingleQuote;
      continue;
    }

    if (ch === '"' && !inSingleQuote) {
      inDoubleQuote = !inDoubleQuote;
      continue;
    }

    if (ch === '#' && !inSingleQuote && !inDoubleQuote) {
      return val.slice(0, i).trim();
    }
  }

  return val.trim();
}

export function loadEnv({ silent = false } = {}) {
  const hermesHome = process.env.HERMES_HOME;
  const hermesProfile = process.env.HERMES_PROFILE;
  const candidates = [
    path.join(SKILL_DIR, '.env'),
    path.join(process.cwd(), '.env'),
    hermesHome ? path.join(hermesHome, '.env') : null,
    hermesProfile ? path.join(os.homedir(), '.hermes', 'profiles', hermesProfile, '.env') : null,
    path.join(os.homedir(), '.hermes', '.env'),
    path.join(os.homedir(), '.openclaw', '.env'),
    path.join(os.homedir(), '.env'),
  ].filter(Boolean);

  for (const envPath of candidates) {
    if (fs.existsSync(envPath)) {
      if (!silent) console.log(`Loading env from: ${envPath}`);
      const content = fs.readFileSync(envPath, 'utf-8');
      for (const line of content.split('\n')) {
        let trimmed = line.trim();
        if (!trimmed || trimmed.startsWith('#')) continue;
        // Strip leading "export " (common in shell-style .env files)
        if (trimmed.startsWith('export ')) trimmed = trimmed.slice(7).trim();
        const eqIdx = trimmed.indexOf('=');
        if (eqIdx < 0) continue;
        let key = trimmed.slice(0, eqIdx).trim();
        let val = trimmed.slice(eqIdx + 1).trim();
        // Remove inline comments (# not inside quotes)
        val = stripInlineComment(val);
        // Unquote values: "foo" or 'foo' → foo
        if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
          val = val.slice(1, -1);
        }
        // Only set if not already defined in environment
        if (process.env[key] === undefined) {
          process.env[key] = val;
        }
      }
      return;
    }
  }
  if (!silent) console.log('No .env file found in standard locations.');
}

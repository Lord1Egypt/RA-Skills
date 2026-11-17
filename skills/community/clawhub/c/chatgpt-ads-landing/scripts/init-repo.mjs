#!/usr/bin/env node
/**
 * Create a landing-page repo from the engine template bundled with this skill.
 *
 *   node init-repo.mjs <target-dir>
 *
 * Refuses to touch a directory that already has files, so it can never
 * overwrite an existing repo. Prefer the user's existing landing-page repo when it
 * is on this machine; use this only where there is none.
 */
import { cpSync, existsSync, readdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const here = dirname(fileURLToPath(import.meta.url));
const target = process.argv[2] && resolve(process.argv[2]);
if (!target) { console.error('usage: node init-repo.mjs <target-dir>'); process.exit(1); }
if (existsSync(target) && readdirSync(target).length) {
  console.error(`✖ ${target} is not empty — refusing to overwrite. Use new-page.mjs to add a page to an existing repo.`);
  process.exit(1);
}

cpSync(join(here, '..', 'assets', 'engine'), target, { recursive: true });
try {
  execFileSync('git', ['init', '-q'], { cwd: target });
} catch (e) {
  console.warn('⚠ git init failed; the files are in place anyway');
}
console.log(`✔ engine copied to ${target}
next: node ${join(here, 'new-page.mjs')} ${target} <slug>`);

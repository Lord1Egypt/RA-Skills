#!/usr/bin/env node
/**
 * Add a page to a landing-page repo from the skill's starter page.
 *
 *   node new-page.mjs <repo-dir> <slug>
 *
 * slug = lowercase letters, digits, dashes (it becomes pages/<slug>/ and the
 * zip name). Never overwrites an existing page.
 */
import { cpSync, existsSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const [repoArg, slug] = process.argv.slice(2);
if (!repoArg || !slug) { console.error('usage: node new-page.mjs <repo-dir> <slug>'); process.exit(1); }
if (!/^[a-z0-9][a-z0-9-]*$/.test(slug)) { console.error(`✖ bad slug "${slug}": use lowercase letters, digits and dashes`); process.exit(1); }

const repo = resolve(repoArg);
if (!existsSync(join(repo, 'scripts', 'build.js')) || !existsSync(join(repo, 'shared', 'lp.js'))) {
  console.error(`✖ ${repo} does not look like a landing-page repo (no scripts/build.js + shared/lp.js). Run init-repo.mjs first.`);
  process.exit(1);
}
const dest = join(repo, 'pages', slug);
if (existsSync(dest)) { console.error(`✖ ${dest} already exists — refusing to overwrite`); process.exit(1); }

cpSync(join(here, '..', 'assets', 'starter-page'), dest, { recursive: true });
console.log(`✔ created ${dest}
fill every 填【…】 in page.json and index.html, then:
  cd "${repo}" && node scripts/package.js ${slug} --force   # first deploy only (url still a placeholder)`);

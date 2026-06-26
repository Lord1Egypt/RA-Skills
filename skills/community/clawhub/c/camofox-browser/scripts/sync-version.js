#!/usr/bin/env node
/**
 * Sync openclaw.plugin.json version with package.json.
 * Run via: npm run version:sync
 * Auto-runs on npm version via the "version" lifecycle script.
 */

import { readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');

const pkg = JSON.parse(await readFile(join(root, 'package.json'), 'utf8'));
const pluginPath = join(root, 'openclaw.plugin.json');
const plugin = JSON.parse(await readFile(pluginPath, 'utf8'));

if (plugin.version !== pkg.version) {
  plugin.version = pkg.version;
  await writeFile(pluginPath, JSON.stringify(plugin, null, 2) + '\n');
  console.log(`openclaw.plugin.json version synced to ${pkg.version}`);
} else {
  console.log(`openclaw.plugin.json already at ${pkg.version}`);
}

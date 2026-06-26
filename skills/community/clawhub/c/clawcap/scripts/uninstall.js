#!/usr/bin/env node

/**
 * ClawCap Uninstall Script
 *
 * What this script does:
 *   1. If a backup exists at ~/.openclaw/openclaw.json.backup, restores it
 *   2. If no backup, removes ClawCap URLs from the config and restores originals
 *
 * What this script does NOT do:
 *   - It does NOT delete any files (backup is renamed, not deleted)
 *   - It does NOT modify any files outside ~/.openclaw/
 *   - It does NOT run any network requests
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// Only allow writing within ~/.openclaw/
const ALLOWED_DIR = path.join(os.homedir(), '.openclaw');

function validatePath(filePath) {
  const resolved = path.resolve(filePath);
  if (!resolved.startsWith(ALLOWED_DIR)) {
    console.error('Error: Refusing to write outside ~/.openclaw/ directory.');
    process.exit(1);
  }
  return resolved;
}

function main() {
  console.log('');
  console.log('ClawCap Uninstall');
  console.log('=================');
  console.log('');

  const configPath = validatePath(path.join(ALLOWED_DIR, 'openclaw.json'));
  const backupPath = validatePath(configPath + '.backup');

  if (fs.existsSync(backupPath)) {
    // Restore from backup by copying it back (backup is preserved as .backup.old)
    fs.copyFileSync(backupPath, configPath);
    fs.renameSync(backupPath, backupPath + '.old');
    console.log('Restored original config from backup.');
    console.log('ClawCap proxy routing has been removed.');
    console.log(`(Backup moved to ${backupPath}.old)`);
  } else {
    console.log('No backup found. Removing ClawCap URLs from config...');

    if (!fs.existsSync(configPath)) {
      console.log('No OpenClaw config found. Nothing to do.');
      process.exit(0);
    }

    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    let restored = 0;

    function restoreProviders(providers) {
      if (Array.isArray(providers)) {
        for (const p of providers) {
          if (p._originalBaseUrl) {
            p.baseUrl = p._originalBaseUrl;
            delete p._originalBaseUrl;
            restored++;
          }
        }
      } else if (typeof providers === 'object') {
        for (const [, p] of Object.entries(providers)) {
          if (p && p._originalBaseUrl) {
            p.baseUrl = p._originalBaseUrl;
            delete p._originalBaseUrl;
            restored++;
          }
        }
      }
    }

    if (config.models && config.models.providers) restoreProviders(config.models.providers);
    if (config.providers) restoreProviders(config.providers);

    fs.writeFileSync(configPath, JSON.stringify(config, null, 2) + '\n', 'utf8');
    console.log(`Restored ${restored} provider(s) to original URLs.`);
  }

  console.log('');
}

main();

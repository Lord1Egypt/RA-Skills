#!/usr/bin/env node
/**
 * Backup skill CLI entry point
 * 
 * Commands:
 *   openclaw backup run           - Run backup now
 *   openclaw backup status       - Show last backup info
 *   openclaw backup restore       - Interactive restore
 *   openclaw backup enable-cron   - Enable scheduled backup
 *   openclaw backup disable-cron  - Disable scheduled backup
 *   openclaw backup set-cron <expr> - Set cron schedule
 */

import { readFileSync } from 'fs';
import { join } from 'path';

const DOT = process.env.OPENCLAW_DIR || process.env.HOME + '/.openclaw';

async function loadConfig() {
  try {
    const configPath = join(DOT, 'skills/claw-saver/config.json');
    return JSON.parse(readFileSync(configPath, 'utf8'));
  } catch {
    return { cron: '0 */5 * * *' };
  }
}

/**
 * Read token from openclaw.json env (set via openclaw config).
 * This is the same token used by the running gateway.
 */
function getBackupToken() {
  try {
    const cfgPath = join(DOT, 'openclaw.json');
    const cfg = JSON.parse(readFileSync(cfgPath, 'utf8'));
    return cfg.env?.OPENCLAW_BACKUP_GIT_TOKEN || '';
  } catch {
    return '';
  }
}

function cronScript(cronExpr) {
  const skillDir = join(DOT, 'skills/claw-saver');
  const token = getBackupToken();
  // Pass token via environment so the cron job can push
  const tokenEnv = token ? `OPENCLAW_BACKUP_GIT_TOKEN=${token}` : '';
  return `${tokenEnv} NODE_PATH=${process.env.NODE_PATH || '/usr/lib/node_modules'} node ${skillDir}/scripts/cli.js run`;
}

/**
 * Enable cron backup
 */
async function enableCron() {
  const config = await loadConfig();
  const cronExpr = config.cron || '0 */5 * * *';
  const script = cronScript(cronExpr);

  // Check if cron already exists
  const { execSync } = await import('child_process');
  try {
    execSync(`crontab -l | grep -q "backup.*cli.js"`, { stdio: 'pipe' });
    console.log('Cron already enabled. Use set-cron to change schedule.');
    return;
  } catch { /* not found */ }

  // Add cron job
  const cronLine = `${cronExpr} ${script}`;
  execSync(`(crontab -l 2>/dev/null; echo "${cronLine}") | crontab -`, { shell: '/bin/bash' });
  console.log(`Cron enabled: ${cronExpr}`);
}

/**
 * Disable cron backup
 */
async function disableCron() {
  const { execSync } = await import('child_process');
  execSync(`crontab -l | grep -v "backup.*cli.js" | crontab -`, { shell: '/bin/bash' });
  console.log('Cron disabled.');
}

/**
 * Set cron schedule
 */
async function setCron(expr) {
  const { execSync } = await import('child_process');

  // Validate cron expression
  if (!expr || !expr.includes('*')) {
    console.error('Invalid cron expression. Example: 0 */2 * * *');
    process.exit(1);
  }

  // Remove old and add new
  execSync(`(crontab -l 2>/dev/null | grep -v "backup.*cli.js"; echo "${expr} ${cronScript(expr)}") | crontab -`, { shell: '/bin/bash' });
  console.log(`Cron schedule updated: ${expr}`);
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  // Lazy import to avoid loading backup.js when not needed
  let runBackup, getBackupStatus, restoreBackup, listBackups;

  switch (command) {
    case 'run': {
      ({ runBackup } = await import('../lib/backup.js'));
      const result = await runBackup();
      if (result.skipped) {
        console.log('Backup skipped: no changes detected.');
      } else {
        console.log(`Backup completed: ${result.commit}`);
      }
      break;
    }

    case 'status': {
      ({ getBackupStatus } = await import('../lib/backup.js'));
      const status = await getBackupStatus();
      if (status.status === 'not_initialized') {
        console.log('Backup not initialized. Run "openclaw backup run" first.');
      } else if (status.status === 'no_commits') {
        console.log('No backups found. Run "openclaw backup run" first.');
      } else {
        console.log(`Last backup: ${status.lastTime}`);
        console.log(`Commit: ${status.lastCommit}`);
      }
      break;
    }

    case 'restore': {
      ({ restoreBackup, listBackups } = await import('../lib/restore.js'));
      console.log('Available backups:');
      const backups = await listBackups();
      backups.forEach((b, i) => console.log(`  ${i + 1}. ${b}`));
      // For now, restore from most recent commit
      if (backups.length > 0) {
        const commit = backups[0].split(' ')[0];
        await restoreBackup(commit, { confirm: false });
      }
      break;
    }

    case 'enable-cron':
      await enableCron();
      break;

    case 'disable-cron':
      await disableCron();
      break;

    case 'set-cron':
      await setCron(args[1]);
      break;

    default:
      console.log(`Usage: openclaw backup <command>

Commands:
  run             Run backup now
  status          Show last backup info
  restore         Restore from backup
  enable-cron     Enable scheduled backup
  disable-cron    Disable scheduled backup
  set-cron <expr> Set cron schedule (e.g. "0 */2 * * *")
`);
      process.exit(1);
  }
}

main().catch((e) => {
  console.error('Error:', e.message);
  process.exit(1);
});
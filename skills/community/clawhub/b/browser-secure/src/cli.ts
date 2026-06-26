#!/usr/bin/env node

import dotenv from 'dotenv';
import { Command } from 'commander';
import { spawn } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Load .env from the parent skills/ directory — kept outside this skill's
// source tree so credentials don't live alongside distributed code.
// Override with BROWSER_SECURE_ENV if a custom location is needed.
{
  const __envFile = fileURLToPath(import.meta.url);
  const skillRoot = path.resolve(path.dirname(__envFile), '..');
  const defaultEnvPath = path.resolve(skillRoot, '..', '.env');
  dotenv.config({ path: process.env.BROWSER_SECURE_ENV || defaultEnvPath });
}
import {
  startBrowser,
  performAction,
  extractData,
  closeBrowser,
  getBrowserStatus,
  suspendSession,
  resumeSession,
  getPage,
  reconnectToDaemon
} from './browser/secure-session.js';
import {
  startDaemon,
  stopDaemon,
  printDaemonStatus,
  getDaemonStatus,
  isDaemonRunning,
  loadDaemonState
} from './browser/daemon.js';
import { readAuditLog, rotateAuditLog } from './security/audit.js';
import {
  logError,
  logLaunchError,
  logNavigationError,
  logVaultError,
  logApprovalError,
  logDaemonError,
  logCredentialError,
  logSessionError,
  readErrorLog,
  getErrorStats,
  clearErrorLog,
  ErrorLevel
} from './utils/error-log.js';
import { loadConfig, saveConfig, getConfigPath, checkCredentialSource } from './config/loader.js';
import { listAvailableVaults, getSiteCredentials } from './vault/index.js';
import { clearCredentialCache } from './security/approval.js';
import { listChromeProfiles, promptProfileSelection, getProfileById, createChromeProfile } from './browser/chrome-profiles.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const program = new Command();

program
  .name('browser-secure')
  .description('Secure browser automation with vault integration')
  .version('1.0.0');

// Welcome page path (used as default)
const WELCOME_PAGE_PATH = `file://${path.join(__dirname, '..', 'assets', 'welcome.html')}`;

// Navigate command
program
  .command('navigate [url]')
  .description('Navigate to a URL (defaults to welcome page if no URL provided)')
  .option('-s, --site <site>', 'Site configuration for authentication')
  .option('--auto-vault', 'Auto-discover credentials from vault (interactive)')
  .option('--headless', 'Run in headless mode')
  .option('-t, --timeout <seconds>', 'Session timeout in seconds', '1800')
  .option('--unattended', 'Run in unattended mode for automation (default: interactive approvals)')
  .option('--interactive', 'Force interactive approvals (default)')
  .option('--skip-approval', 'Skip all approvals including destructive actions (DANGEROUS)')
  .option('--credential-source <source>', 'Credential source for unattended mode (env|vault|cache)', 'vault')
  .option('-p, --profile <profile>', 'Chrome profile to use (id or "select" to choose interactively)')
  .option('--close-chrome', 'Permit browser-secure to quit your running Chrome when --profile requires exclusive access')
  .option('--list-profiles', 'List available Chrome profiles and exit')
  .action(async (url, options) => {
    try {
      // Handle --list-profiles
      if (options.listProfiles) {
        const profiles = listChromeProfiles();
        console.log('\n📋 Available Chrome profiles:\n');
        profiles.forEach((profile, index) => {
          const marker = profile.id === 'Default' ? ' ★' : '';
          console.log(`  ${index + 1}. ${profile.name}${marker}`);
          console.log(`     ID: ${profile.id}`);
          console.log(`     Path: ${profile.path}`);
          console.log('');
        });
        process.exit(0);
      }

      // Determine mode: unattended must be explicit; interactive is the default
      const isUnattended = options.unattended === true && options.interactive !== true;

      // Validate credential source for unattended mode
      const credentialSource = options.credentialSource;
      if (!['env', 'vault', 'cache'].includes(credentialSource)) {
        console.error(`Error: Invalid credential source "${credentialSource}". Must be one of: env, vault, cache`);
        process.exit(1);
      }

      if (isUnattended) {
        const sourceCheck = checkCredentialSource(credentialSource);
        if (!sourceCheck.valid) {
          logCredentialError(`Credential check failed: ${sourceCheck.error}`, undefined, false);
          console.error(`Error: ${sourceCheck.error}`);
          process.exit(1);
        }
      }

      // Handle profile selection
      let selectedProfile = null;
      if (options.profile) {
        if (options.profile === 'select') {
          selectedProfile = await promptProfileSelection();
        } else {
          selectedProfile = getProfileById(options.profile);
          if (selectedProfile) {
            console.log(`✅ Using profile: ${selectedProfile.name} [${selectedProfile.id}]`);
          } else {
            console.log(`⚠️  Profile "${options.profile}" not found, using incognito mode`);
            console.log('   Run with --list-profiles to see available profiles');
          }
        }
      }

      // Use welcome page as default if no URL provided
      const targetUrl = url || WELCOME_PAGE_PATH;
      if (!url) {
        console.log('🦞 No URL provided, opening welcome page...');
      }

      await startBrowser(targetUrl, {
        site: options.site,
        autoVault: options.autoVault,
        headless: options.headless,
        timeout: parseInt(options.timeout) * 1000,
        profile: selectedProfile || undefined,
        closeChrome: options.closeChrome === true,
        unattended: isUnattended ? {
          enabled: true,
          credentialSource: credentialSource,
          skipApproval: options.skipApproval === true
        } : undefined
      });

      // In daemon mode the CDP connection keeps the process alive.
      // Disconnect cleanly so the CLI exits, but keep the page open in Chrome
      // so subsequent act/extract/screenshot commands can reconnect to it.
      const { closeBrowser } = await import('./browser/secure-session.js');
      await closeBrowser({ keepPage: true });
    } catch (e) {
      const err = e instanceof Error ? e : new Error(String(e));
      logLaunchError(`Failed to start browser for navigate: ${url ?? 'welcome page'}`, err, {
        url: url ?? 'welcome page',
        profile: options.profile,
      });
      console.error(`Error: ${err.message}`);
      process.exit(1);
    }
  });

// Act command
program
  .command('act <instruction>')
  .description('Perform a natural language action')
  .option('-y, --yes', 'Auto-approve without prompting (deprecated: use --unattended)')
  .option('--unattended', 'Run in unattended mode for automation (default: interactive approvals)')
  .option('--interactive', 'Force interactive approvals (default)')
  .option('--skip-approval', 'Skip all approvals including destructive actions (DANGEROUS)')
  .action(async (instruction, options) => {
    try {
      const { reconnectToDaemon, performAction, closeBrowser } = await import('./browser/secure-session.js');

      // Reconnect to running daemon (or fail cleanly if none)
      await reconnectToDaemon();

      // Determine mode: unattended must be explicit; interactive is the default
      const isUnattended = options.unattended === true && options.interactive !== true;

      await performAction(instruction, {
        autoApprove: options.yes,
        unattended: isUnattended ? {
          enabled: true,
          credentialSource: 'vault',
          skipApproval: options.skipApproval === true
        } : undefined
      });

      // Keep page open for subsequent commands; use 'browser-secure close' to end
      await closeBrowser({ keepPage: true });
    } catch (e) {
      const err = e instanceof Error ? e : new Error(String(e));
      logSessionError(`Failed to perform action: ${instruction}`, err);
      console.error(`Error: ${err.message}`);
      process.exit(1);
    }
  });

// Extract command
program
  .command('extract <instruction>')
  .description('Extract data from the page')
  .option('-s, --schema <json>', 'JSON schema for extraction')
  .action(async (instruction, options) => {
    try {
      const { reconnectToDaemon, extractData, closeBrowser } = await import('./browser/secure-session.js');
      await reconnectToDaemon();

      const schema = options.schema ? JSON.parse(options.schema) : undefined;
      const result = await extractData(instruction, schema);
      console.log(JSON.stringify(result, null, 2));

      await closeBrowser({ keepPage: true });
    } catch (e) {
      console.error(`Error: ${e}`);
      process.exit(1);
    }
  });

// Screenshot command
program
  .command('screenshot')
  .description('Take a screenshot of the current page')
  .action(async () => {
    try {
      const { reconnectToDaemon, takeScreenshot, closeBrowser } = await import('./browser/secure-session.js');
      await reconnectToDaemon();

      const screenshotPath = await takeScreenshot('manual');
      if (screenshotPath) {
        console.log(`Screenshot saved: ${screenshotPath}`);
      }

      await closeBrowser({ keepPage: true });
    } catch (e) {
      console.error(`Error: ${e}`);
      process.exit(1);
    }
  });

// Close command
program
  .command('close')
  .description('Close the browser and clean up')
  .action(async () => {
    try {
      await closeBrowser();
    } catch (e) {
      console.error(`Error: ${e}`);
      process.exit(1);
    }
  });

// Suspend command
program
  .command('suspend')
  .description('Suspend the current session (pause timeout)')
  .action(() => {
    try {
      suspendSession();
    } catch (e) {
      console.error(`Error: ${e}`);
      process.exit(1);
    }
  });

// Resume command
program
  .command('resume')
  .description('Resume the current session (continue timeout)')
  .action(() => {
    try {
      resumeSession();
    } catch (e) {
      console.error(`Error: ${e}`);
      process.exit(1);
    }
  });

// Status command
program
  .command('status')
  .description('Show current session and daemon status')
  .action(() => {
    const status = getBrowserStatus();
    const daemon = getDaemonStatus();

    // Show daemon status first
    if (daemon) {
      console.log('Daemon: RUNNING');
      console.log(`  Profile: ${daemon.profile} [${daemon.profileId}]`);
      console.log(`  PID: ${daemon.pid}`);
      console.log(`  CDP port: ${daemon.port}`);
      console.log('');
    } else if (isDaemonRunning()) {
      console.log('Daemon: STALE (run: browser-secure daemon stop to clean up)');
      console.log('');
    }

    if (status.active) {
      console.log('Session: ACTIVE');
      console.log(`  ID: ${status.sessionId}`);
      console.log(`  Site: ${status.site || 'N/A'}`);
      console.log(`  Time remaining: ${status.timeRemaining}s`);
      console.log(`  Actions: ${status.actionCount}`);
      console.log(`  Suspended: ${status.suspended ? 'Yes' : 'No'}`);
    } else {
      console.log('Session: INACTIVE');
    }
  });

// Audit command
program
  .command('audit')
  .description('View audit logs')
  .option('-s, --session <id>', 'Show specific session')
  .option('--tail <n>', 'Show last N sessions', '10')
  .action((options) => {
    try {
      const sessions = readAuditLog(options.session);
      const tail = parseInt(options.tail);

      const display = sessions.slice(-tail);

      for (const session of display) {
        console.log('\n' + '='.repeat(60));
        console.log(`Session: ${session.sessionId}`);
        console.log(`Time: ${session.timestamp}`);
        console.log(`Site: ${session.site || 'N/A'}`);
        console.log(`Duration: ${session.session.duration}s`);
        console.log(`Actions: ${session.actions.length}`);
        console.log(`Chain Hash: ${session.chainHash.slice(0, 16)}...`);

        if (session.actions.length > 0) {
          console.log('\n  Actions:');
          for (const action of session.actions) {
            console.log(`    - ${action.action} (${action.timestamp})`);
          }
        }
      }
    } catch (e) {
      console.error(`Error: ${e}`);
      process.exit(1);
    }
  });

// Config command
program
  .command('config')
  .description('Show or edit configuration')
  .option('--path', 'Show config file path')
  .option('--edit', 'Open config in editor')
  .action((options) => {
    if (options.path) {
      console.log(getConfigPath());
      return;
    }

    if (options.edit) {
      const editor = process.env.EDITOR || 'nano';
      const child = spawn(editor, [getConfigPath()], { stdio: 'inherit' });
      child.on('close', (code) => {
        process.exit(code || 0);
      });
      return;
    }

    const config = loadConfig();
    console.log('Current Configuration:');
    console.log(JSON.stringify(config, null, 2));
  });

// Vault command
program
  .command('vault')
  .description('Vault management')
  .option('-l, --list', 'List available vaults')
  .option('-t, --test <site>', 'Test vault credentials for a site')
  .action(async (options) => {
    if (options.list) {
      const vaults = listAvailableVaults();
      console.log('Available vaults:');
      for (const vault of vaults) {
        console.log(`  - ${vault}`);
      }
      return;
    }

    if (options.test) {
      try {
        const creds = await getSiteCredentials(options.test);
        console.log(`Credentials for ${options.test}:`);
        console.log(`  Username: ${creds.username ? '***' : 'N/A'}`);
        console.log(`  Password: ${creds.password ? '***' : 'N/A'}`);
        console.log(`  Token: ${creds.token ? '***' : 'N/A'}`);
      } catch (e) {
        console.error(`Failed to get credentials: ${e}`);
        process.exit(1);
      }
      return;
    }

    console.log('Use --list or --test <site>');
  });

// Cache command
program
  .command('cache')
  .description('Credential cache management')
  .option('-c, --clear', 'Clear the credential cache')
  .option('-s, --status', 'Show cache status')
  .action((options) => {
    if (options.clear) {
      clearCredentialCache();
      console.log('Credential cache cleared.');
      return;
    }

    if (options.status) {
      const config = loadConfig();
      console.log('Credential Cache Status:');
      console.log(`  Cache duration: ${config.security.session.credentialCacheMinutes} minutes`);
      console.log(`  Encryption: AES-256-GCM`);
      console.log(`  Cache directory: ~/.browser-secure/cache/`);
      return;
    }

    console.log('Use --clear to clear cache or --status to show cache info');
  });

// Profile command
program
  .command('profile')
  .description('Chrome profile management')
  .option('-l, --list', 'List available Chrome profiles')
  .option('-c, --create <name>', 'Create a new Chrome profile with welcome page')
  .option('--launch', 'Launch Chrome with the profile after creation')
  .action(async (options) => {
    if (options.list) {
      const profiles = listChromeProfiles();
      console.log('\n📋 Available Chrome profiles:\n');
      profiles.forEach((profile, index) => {
        const marker = profile.id === 'Default' ? ' ★' : '';
        console.log(`  ${index + 1}. ${profile.name}${marker}`);
        console.log(`     ID: ${profile.id}`);
        console.log(`     Path: ${profile.path}`);
        console.log('');
      });
      return;
    }

    if (options.create) {
      try {
        const profileName = options.create;
        console.log(`\n🔧 Creating Chrome profile: "${profileName}"...\n`);
        
        const profile = createChromeProfile(profileName);
        
        console.log('✅ Profile created successfully!\n');
        console.log(`   Name: ${profile.name}`);
        console.log(`   ID: ${profile.id}`);
        console.log(`   Path: ${profile.path}`);
        console.log(`   Welcome page: ${profile.welcomePage}`);
        console.log('\n📋 Next steps:');
        console.log('   1. Chrome will open with a welcome page');
        console.log('   2. Install the Bitwarden extension');
        console.log('   3. Install the OpenClaw Browser Relay extension');
        console.log('   4. Log in to your password vault');
        console.log('\n   Use this profile: browser-secure navigate <url> --profile "' + profile.id + '"');
        
        if (options.launch) {
          console.log('\n🚀 Launching Chrome...\n');
          const chromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
          const child = spawn(chromePath, [`--profile-directory=${profile.id}`], {
            detached: true,
            stdio: 'ignore'
          });
          child.unref();
        }
      } catch (e) {
        console.error(`Error creating profile: ${e}`);
        process.exit(1);
      }
      return;
    }

    console.log('Use --list to list profiles or --create <name> to create a new profile');
  });

// Daemon command
program
  .command('daemon')
  .description('Manage the persistent Chrome daemon')
  .argument('[subcommand]', 'start, stop, or status')
  .option('-s, --start', 'Start the daemon (defaults to Default profile)')
  .option('-S, --stop', 'Stop the daemon')
  .option('--status', 'Show daemon status')
  .option('-p, --profile <name>', 'Profile to use when starting daemon (id or name)')
  .option('--close-chrome', 'Permit browser-secure to quit your running Chrome (required in --unattended mode)')
  .option('--unattended', 'Unattended mode: no prompts; requires --close-chrome if Chrome is running')
  .action(async (subcommand, options) => {
    const cmd = subcommand ?? (options.stop ? 'stop' : options.status ? 'status' : null);

    if (cmd === 'stop') {
      await stopDaemon();
      return;
    }
    if (cmd === 'status') {
      printDaemonStatus();
      return;
    }
    if (cmd === 'start' || options.start || options.profile) {
      try {
        await startDaemon({
          profileId: options.profile,
          closeChrome: options.closeChrome === true,
          isUnattended: options.unattended === true,
        });
      } catch (e: any) {
        const err = e instanceof Error ? e : new Error(String(e));
        logDaemonError(`Daemon start failed for profile "${options.profile ?? 'Default'}"`, err);
        console.error(`Error: ${err.message}`);
        process.exit(1);
      }
      return;
    }

    // No args: show status
    printDaemonStatus();
  });

// Errors command
program
  .command('errors')
  .description('View and manage error logs')
  .option('--stats', 'Show error statistics')
  .option('--type <name>', 'Filter by error type (e.g. LaunchError, NavigationError)')
  .option('--level <level>', 'Filter by level (ERROR, WARN, INFO, DEBUG)')
  .option('--since <date>', 'Show errors since date (ISO format)')
  .option('--limit <n>', 'Limit number of entries shown', '50')
  .option('--clear', 'Clear the error log')
  .action((options) => {
    if (options.clear) {
      clearErrorLog();
      console.log('✅ Error log cleared');
      return;
    }

    if (options.stats) {
      const stats = getErrorStats();
      console.log(`Total errors: ${stats.total}`);
      if (stats.total === 0) return;
      console.log('\nBy type:');
      for (const [t, n] of Object.entries(stats.byType)) {
        console.log(`  ${t}: ${n}`);
      }
      console.log('\nBy level:');
      for (const [l, n] of Object.entries(stats.byLevel)) {
        console.log(`  ${l}: ${n}`);
      }
      return;
    }

    const entries = readErrorLog({
      level: options.level as ErrorLevel | undefined,
      errorType: options.type,
      since: options.since,
      limit: parseInt(options.limit),
    });

    if (entries.length === 0) {
      console.log('No errors found.');
      return;
    }

    for (const e of entries) {
      const icon = e.level === 'ERROR' ? '❌' : e.level === 'WARN' ? '⚠️' : 'ℹ️';
      console.log(`\n${icon} [${e.level}] ${e.errorType}`);
      console.log(`   ${e.timestamp}${e.sessionId ? ` | session: ${e.sessionId}` : ''}`);
      console.log(`   ${e.message}`);
      if (e.context) {
        for (const [k, v] of Object.entries(e.context)) {
          console.log(`   ${k}: ${v}`);
        }
      }
      if (e.stack) {
        const firstLine = e.stack.split('\n')[0];
        if (firstLine) console.log(`   stack: ${firstLine.trim()}`);
      }
    }
    console.log(`\nShowing ${entries.length} of ${entries.length} entries. Run with --help for filters.`);
  });

// Cleanup command
program
  .command('cleanup')
  .description('Clean up old audit logs and temporary files')
  .option('-d, --days <n>', 'Retention days', '30')
  .action((options) => {
    try {
      rotateAuditLog(parseInt(options.days));
      console.log(`Audit logs rotated (retention: ${options.days} days)`);
    } catch (e) {
      console.error(`Error: ${e}`);
      process.exit(1);
    }
  });

// Handle graceful shutdown
process.on('SIGINT', async () => {
  console.log('\n\nReceived SIGINT, cleaning up...');
  await closeBrowser();
  process.exit(0);
});

process.on('SIGTERM', async () => {
  await closeBrowser();
  process.exit(0);
});

// Global error handlers — never let errors disappear silently
process.on('uncaughtException', (err: Error) => {
  logSessionError(`Uncaught exception: ${err.message}`, err);
  console.error(`\n❌ Uncaught exception: ${err.message}`);
  if (process.env.DEBUG) {
    console.error(err.stack);
  }
  process.exit(1);
});

process.on('unhandledRejection', (reason: unknown) => {
  const msg = reason instanceof Error ? reason.message : String(reason);
  const err = reason instanceof Error ? reason : undefined;
  logSessionError(`Unhandled promise rejection: ${msg}`, err);
  console.error(`\n❌ Unhandled rejection: ${msg}`);
  if (process.env.DEBUG) {
    console.error(reason);
  }
});

// ─── Init command: onboard a new site ───────────────────────────────────────
program
  .command('init <url>')
  .description('Onboard a new site: analyze structure, detect login/search, record profile')
  .option('-n, --name <name>', 'Site display name')
  .option('-p, --profile <profile>', 'Chrome profile to use', 'Default')
  .option('-y, --yes', 'Auto-approve all prompts')
  .action(async (url, options) => {
    try {
      const readline = await import('readline');
      const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
      const ask = (q: string): Promise<string> => new Promise(resolve => rl.question(q, resolve));

      // Ensure daemon is running
      const daemonState = loadDaemonState();
      if (!daemonState || !isDaemonRunning(daemonState)) {
        console.log('🚀 Starting daemon...');
        await startDaemon({ profileId: options.profile });
      }

      // Connect to daemon
      await reconnectToDaemon();
      const page = getPage();
      if (!page) throw new Error('Failed to connect to browser');

      // Navigate to target URL
      console.log(`\n🌐 Navigating to ${url}...`);
      await page.goto(url, { waitUntil: 'domcontentloaded' });
      await new Promise(r => setTimeout(r, 3000));

      // Analyze site
      const { analyzeSite, buildSiteProfile } = await import('./research/site-profiler.js');
      const analysis = await analyzeSite(page, url);

      console.log('\n📊 Site Analysis');
      console.log('─────────────────');
      console.log(`Login required: ${analysis.hasLoginForm ? 'YES' : 'No'}`);
      console.log(`Search available: ${analysis.hasSearch ? 'YES' : 'No'}`);
      if (analysis.searchSelector) console.log(`  Search selector: ${analysis.searchSelector}`);
      console.log(`Navigation links found: ${analysis.navigation.length}`);
      analysis.navigation.slice(0, 5).forEach(n => console.log(`  - ${n.name}: ${n.url}`));
      console.log(`Content links found: ${analysis.contentLinks.length}`);
      console.log(`Screenshots saved:`);
      analysis.screenshots.forEach(s => console.log(`  - ${s}`));

      // HIL: confirm accessing this site at all
      if (!options.yes) {
        const ans = await ask(`\n⚠️  Approve accessing this site for data capture? [Y/n]: `);
        if (/^n(o)?$/i.test(ans.trim())) {
          console.log('Aborted. Site access not approved.');
          rl.close();
          await closeBrowser();
          return;
        }
      }

      // HIL: confirm login requirement
      let loginRequired = analysis.hasLoginForm;
      if (!options.yes) {
        const ans = await ask(`\n⚠️  Is login required for this site? [${loginRequired ? 'Y/n' : 'y/N'}]: `);
        loginRequired = /^y(es)?$/i.test(ans.trim()) || (loginRequired && !/^n(o)?$/i.test(ans.trim()));
      }

      // Extract sample content if available
      let sampleExcerpt: string | undefined;
      if (analysis.contentLinks.length > 0) {
        const { extractContent } = await import('./research/content-extractor.js');
        try {
          await page.goto(analysis.contentLinks[0], { waitUntil: 'domcontentloaded', timeout: 15000 });
          await new Promise(r => setTimeout(r, 3000));
          const content = await extractContent(page);
          sampleExcerpt = content.excerpt;
          console.log('\n📝 Sample content extracted:');
          console.log(`  Title: ${content.title}`);
          console.log(`  Words: ${content.wordCount}`);
          console.log(`  Excerpt: ${content.excerpt.slice(0, 200)}...`);
        } catch {
          console.log('\n⚠️  Could not extract sample content');
        }
      }

      // Build and preview playbook
      const { buildPlaybook } = await import('./research/site-profiler.js');
      const playbook = buildPlaybook(analysis, loginRequired);

      console.log('\n📋 Playbook (hardened steps for future captures):');
      console.log(`  Discovery: ${playbook.discovery.method}`);
      if (playbook.discovery.search_url) console.log(`  Search URL: ${playbook.discovery.search_url}`);
      if (playbook.discovery.search_input_selector) console.log(`  Search input: ${playbook.discovery.search_input_selector}`);
      console.log(`  Access: login=${playbook.access.login_required}`);
      if (playbook.extraction.body_selector) console.log(`  Body selector: ${playbook.extraction.body_selector}`);

      // HIL: confirm recording
      if (!options.yes) {
        const ans = await ask('\n💾 Record this site profile and playbook? [Y/n]: ');
        if (/^n(o)?$/i.test(ans.trim())) {
          console.log('Aborted. Site profile not recorded.');
          rl.close();
          await closeBrowser();
          return;
        }
      }

      // Build and save profile
      const profile = buildSiteProfile(url, analysis, loginRequired, sampleExcerpt);
      if (options.name) profile.name = options.name;

      const { saveSiteProfile } = await import('./research/scrapbook.js');
      saveSiteProfile(profile);

      console.log(`\n✅ Site profile recorded: ${profile.id}`);
      console.log(`   Playbook: ${playbook.discovery.method} → ${playbook.extraction.body_selector || 'auto'}`);
      console.log(`   Scrapbook: ~/.browser-secure/scrapbook/site-profiles.yaml`);

      rl.close();
      await closeBrowser();
    } catch (e) {
      const err = e instanceof Error ? e : new Error(String(e));
      console.error(`Error: ${err.message}`);
      process.exit(1);
    }
  });

// ─── Capture command: extract content from a URL ────────────────────────────
program
  .command('capture <url>')
  .description('Capture content from a URL using recorded site profile')
  .option('-s, --site <siteId>', 'Site profile ID (from init)')
  .option('-p, --profile <profile>', 'Chrome profile to use', 'Default')
  .option('-y, --yes', 'Auto-approve all prompts')
  .option('--full-text', 'Save full text instead of excerpt')
  .option('--save-html', 'Save raw page HTML alongside screenshot')
  .action(async (url, options) => {
    try {
      const readline = await import('readline');
      const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
      const ask = (q: string): Promise<string> => new Promise(resolve => rl.question(q, resolve));

      const { getSiteProfile, urlAlreadyCaptured } = await import('./research/scrapbook.js');

      // Dedup check
      if (urlAlreadyCaptured(url)) {
        console.log('⏭️  URL already captured. Skipping.');
        rl.close();
        return;
      }

      // Determine site profile
      let siteId = options.site;
      if (!siteId) {
        try {
          const hostname = new URL(url).hostname.replace(/^www\./, '').replace(/\./g, '-');
          const profile = getSiteProfile(hostname);
          if (profile) {
            siteId = profile.id;
            console.log(`🔍 Auto-detected site profile: ${siteId}`);
          }
        } catch { /* ignore URL parse errors */ }
      }

      if (!siteId) {
        console.error('Error: No site profile found. Run `browser-secure init <url>` first, or pass --site <id>');
        rl.close();
        process.exit(1);
      }

      const profile = getSiteProfile(siteId);
      if (!profile) {
        console.error(`Error: Site profile "${siteId}" not found`);
        rl.close();
        process.exit(1);
      }

      // Show playbook if available
      if (profile.playbook) {
        console.log('\n📋 Using playbook:');
        console.log(`  Discovery: ${profile.playbook.discovery.method}`);
        console.log(`  Extraction: ${profile.playbook.extraction.body_selector || 'auto-detect'}`);
      }

      // HIL: approve site access
      if (!options.yes) {
        const ans = await ask(`\n⚠️  Approve accessing ${siteId} to capture content? [Y/n]: `);
        if (/^n(o)?$/i.test(ans.trim())) {
          console.log('Aborted. Site access not approved.');
          rl.close();
          return;
        }
      }

      // Ensure daemon
      const daemonState = loadDaemonState();
      if (!daemonState || !isDaemonRunning(daemonState)) {
        await startDaemon({ profileId: options.profile });
      }

      // Connect and navigate
      await reconnectToDaemon();
      const page = getPage();
      if (!page) throw new Error('Failed to connect to browser');

      console.log(`\n🌐 Navigating to ${url}...`);
      await page.goto(url, { waitUntil: 'domcontentloaded' });
      await new Promise(r => setTimeout(r, 3000));

      // Login if required
      let credentialsUsed = false;
      if (profile.login_required) {
        const hasPassword = await page.$('input[type="password"]');
        if (hasPassword) {
          if (!options.yes) {
            const ans = await ask(`\n🔐 Login detected. Use vault credentials for ${siteId}? [y/N]: `);
            if (!/^y(es)?$/i.test(ans.trim())) {
              console.log('Aborted. Login not approved.');
              rl.close();
              await closeBrowser();
              return;
            }
          }

          const { handleSiteAuthentication } = await import('./browser/secure-session.js');
          await handleSiteAuthentication(siteId, { enabled: false, credentialSource: 'vault' });
          credentialsUsed = true;
          await new Promise(r => setTimeout(r, 2000));
        }
      }

      // HIL: approve extraction
      if (!options.yes) {
        const ans = await ask(`\n⚠️  Approve extracting content from this page? [Y/n]: `);
        if (/^n(o)?$/i.test(ans.trim())) {
          console.log('Aborted. Extraction not approved.');
          rl.close();
          await closeBrowser();
          return;
        }
      }

      // Extract content
      const { capturePage, getCapturePreview } = await import('./research/capture-workflow.js');
      const result = await capturePage(page, url, siteId, credentialsUsed, {
        autoApproved: options.yes === true,
        saveFullText: options.fullText === true,
        saveHtml: options.saveHtml === true,
      });

      // HIL: confirm recording
      console.log('\n' + getCapturePreview(result.capture));
      if (!options.yes) {
        const ans = await ask('\n💾 Record this capture? [Y/n]: ');
        if (/^n(o)?$/i.test(ans.trim())) {
          console.log('Aborted. Capture not recorded.');
          rl.close();
          await closeBrowser();
          return;
        }
      }

      const { saveCapture } = await import('./research/scrapbook.js');
      saveCapture(result.capture);

      console.log(`\n✅ Capture recorded: ${result.capture.id}`);
      console.log(`   Screenshot: ${result.screenshotPath}`);
      if (result.htmlPath) console.log(`   HTML: ${result.htmlPath}`);
      if (result.capture.approval_chain) {
        const auto = Object.values(result.capture.approval_chain).some(a => a?.auto);
        if (auto) console.log(`   Approval: auto-approved (--yes)`);
      }

      rl.close();
      await closeBrowser();
    } catch (e) {
      const err = e instanceof Error ? e : new Error(String(e));
      console.error(`Error: ${err.message}`);
      process.exit(1);
    }
  });

// ─── Scrapbook command: view/manage captures ────────────────────────────────
program
  .command('scrapbook')
  .description('View and manage scrapbook captures')
  .option('-l, --list', 'List all captures')
  .option('--sites', 'List site profiles')
  .option('--export <format>', 'Export scrapbook (markdown, json)')
  .option('--output <path>', 'Export file path')
  .action(async (options) => {
    const {
      listCaptures, listSiteProfiles, exportToMarkdown, exportToJson
    } = await import('./research/scrapbook.js');

    if (options.sites) {
      const sites = listSiteProfiles();
      console.log('\n📋 Site Profiles:\n');
      for (const s of sites) {
        console.log(`  ${s.name} [${s.id}]`);
        console.log(`    URL: ${s.url}`);
        console.log(`    Login: ${s.login_required ? 'required' : 'not required'}`);
        console.log(`    Search: ${s.search?.available ? 'available' : 'not available'}`);
        console.log(`    Inited: ${s.init_confirmed_at || 'unknown'}`);
        console.log('');
      }
      return;
    }

    if (options.list || (!options.export)) {
      const captures = listCaptures();
      console.log('\n📋 Scrapbook Captures:\n');
      if (captures.length === 0) {
        console.log('  No captures yet.');
        return;
      }
      for (const c of captures) {
        console.log(`  [${c.id}] ${c.title || 'Untitled'}`);
        console.log(`    Source: ${c.site_id} | Words: ${c.word_count || 0}`);
        console.log(`    URL: ${c.url}`);
        console.log(`    Captured: ${c.captured_at}`);
        console.log('');
      }
      return;
    }

    if (options.export === 'markdown') {
      const md = exportToMarkdown();
      const outPath = options.output || 'scrapbook-export.md';
      fs.writeFileSync(outPath, md);
      console.log(`✅ Exported to ${outPath}`);
      return;
    }

    if (options.export === 'json') {
      const json = exportToJson();
      const outPath = options.output || 'scrapbook-export.json';
      fs.writeFileSync(outPath, json);
      console.log(`✅ Exported to ${outPath}`);
      return;
    }

    console.error('Error: Unknown export format. Use: markdown, json');
    process.exit(1);
  });

program.parse();

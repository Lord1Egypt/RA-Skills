#!/usr/bin/env node
/**
 * Test wrapper for cross-border-intel TypeScript skill
 * This script allows testing the skill directly in OpenClaw environment
 *
 * Usage:
 *   node test-wrapper.mjs [command] [args...]
 *
 * Commands:
 *   add asin <asin> [domain]     - Add Amazon ASIN to watchlist
 *   add keyword <keyword>        - Add TikTok keyword to watchlist
 *   list                         - List all watchlist items
 *   scan amazon                  - Run Amazon scan
 *   scan tiktok                  - Run TikTok scan
 *   report daily                 - Generate daily report
 *   report weekly                - Generate weekly report
 *   health                       - Check skill health
 */

import { createRequire } from 'module';
const require = createRequire(import.meta.url);

// Path to the compiled skill
const SKILL_PATH = '/Users/zhuqiangyi/Beansmile/beansmile-claw-skills/packages/cross-border-intel/dist/index.js';

// Set environment variables for OpenClaw
process.env.OPENCLAW_CONFIG_PATH = process.env.HOME + '/.openclaw/openclaw.json';
process.env.OPENCLAW_STATE_DIR = process.env.HOME + '/.openclaw';

async function main() {
    const args = process.argv.slice(2);
    const command = args[0];

    if (!command || command === 'help' || command === '--help') {
        printHelp();
        return;
    }

    try {
        // Import the skill
        const skill = await import(SKILL_PATH);

        // Initialize database
        await skill.initialize();

        // Execute command
        await executeCommand(skill, command, args.slice(1));
    } catch (error) {
        console.error('Error:', error.message);
        process.exit(1);
    }
}

async function executeCommand(skill, command, args) {
    switch (command) {
        case 'health':
            const health = skill.healthCheck();
            console.log(JSON.stringify(health, null, 2));
            break;

        case 'add': {
            const type = args[0];
            const value = args[1];
            const domain = args[2] || 'com';

            if (!type || !value) {
                console.error('Usage: node test-wrapper.mjs add <asin|keyword> <value> [domain]');
                return;
            }

            if (type === 'asin') {
                const item = await skill.addAmazonWatchlistItem(value, domain);
                console.log('Added Amazon ASIN:', item);
            } else if (type === 'keyword') {
                const item = await skill.addTiktokWatchlistItem(value);
                console.log('Added TikTok keyword:', item);
            } else {
                console.error('Invalid type. Use "asin" or "keyword"');
            }
            break;
        }

        case 'list': {
            const amazonItems = skill.listActiveWatchlists('amazon');
            const tiktokItems = skill.listActiveWatchlists('tiktok');

            console.log('Amazon watchlist (' + amazonItems.length + ' items):');
            amazonItems.forEach(item => {
                console.log('  - ' + item.value + ' (' + item.domain + ')');
            });

            console.log('\nTikTok watchlist (' + tiktokItems.length + ' items):');
            tiktokItems.forEach(item => {
                console.log('  - ' + item.value);
            });
            break;
        }

        case 'scan': {
            const platform = args[0];

            if (platform === 'amazon') {
                console.log('Running Amazon scan...');
                const result = await skill.runAmazonScan();
                console.log(JSON.stringify(result, null, 2));
            } else if (platform === 'tiktok') {
                console.log('Running TikTok scan...');
                const result = await skill.runTiktokScan();
                console.log(JSON.stringify(result, null, 2));
            } else {
                console.error('Usage: node test-wrapper.mjs scan <amazon|tiktok>');
            }
            break;
        }

        case 'report': {
            const type = args[0] || 'daily';

            if (type === 'daily') {
                const report = skill.generateDailyReport();
                console.log(JSON.stringify(report, null, 2));
            } else if (type === 'weekly') {
                const report = skill.generateWeeklyReport();
                console.log(JSON.stringify(report, null, 2));
            } else {
                console.error('Usage: node test-wrapper.mjs report <daily|weekly>');
            }
            break;
        }

        case 'alerts': {
            const alerts = skill.getRecentAlerts(parseInt(args[0]) || 20);
            console.log('Recent alerts (' + alerts.length + '):');
            alerts.forEach(alert => {
                console.log('  - [' + alert.type + '] ' + alert.title);
            });
            break;
        }

        default:
            console.error('Unknown command:', command);
            printHelp();
    }
}

function printHelp() {
    console.log(`
cross-border-intel TypeScript Skill Test Wrapper

Usage:
  node test-wrapper.mjs [command] [args...]

Commands:
  health                    - Check skill health
  add asin <asin> [domain] - Add Amazon ASIN to watchlist
  add keyword <keyword>     - Add TikTok keyword to watchlist
  list                      - List all watchlist items
  scan amazon              - Run Amazon scan
  scan tiktok              - Run TikTok scan
  report daily             - Generate daily report
  report weekly            - Generate weekly report
  alerts [limit]           - Show recent alerts (default: 20)

Examples:
  node test-wrapper.mjs health
  node test-wrapper.mjs add asin B0XXXXXXXXX com
  node test-wrapper.mjs add keyword "kitchen gadgets"
  node test-wrapper.mjs list
  node test-wrapper.mjs scan amazon
  node test-wrapper.mjs report daily
  node test-wrapper.mjs alerts
`);
}

main().catch(console.error);

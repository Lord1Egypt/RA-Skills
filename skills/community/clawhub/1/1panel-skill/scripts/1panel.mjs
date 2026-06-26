#!/usr/bin/env node
/**
 * 1Panel Skill CLI
 * OpenClaw Agent Skill wrapper for 1panel-skill
 */

import { OnePanelClient } from '../dist/index.js';

const args = process.argv.slice(2);
const command = args[0];

// Config from environment
const config = {
  host: process.env.ONEPANEL_HOST || 'localhost',
  port: parseInt(process.env.ONEPANEL_PORT || '8080'),
  apiKey: process.env.ONEPANEL_API_KEY,
  protocol: process.env.ONEPANEL_PROTOCOL || 'http'
};

if (!config.apiKey) {
  console.error('Error: ONEPANEL_API_KEY environment variable is required');
  console.error('');
  console.error('Usage:');
  console.error('  ONEPANEL_API_KEY=xxx 1panel <command> [args]');
  console.error('');
  console.error('Commands:');
  console.error('  containers              List containers');
  console.error('  container <id>          Get container info');
  console.error('  start <id>              Start container');
  console.error('  stop <id>               Stop container');
  console.error('  restart <id>            Restart container');
  console.error('  images                  List images');
  console.error('  websites                List websites');
  console.error('  databases               List databases');
  console.error('  files <path>            List files');
  console.error('  system                  Get system info');
  console.error('  dashboard               Get dashboard info');
  process.exit(1);
}

const client = new OnePanelClient(config);

async function main() {
  try {
    switch (command) {
      case 'containers':
        const containers = await client.containers.list();
        console.log(JSON.stringify(containers, null, 2));
        break;

      case 'container':
        if (!args[1]) {
          console.error('Error: container ID required');
          process.exit(1);
        }
        const container = await client.containers.get(args[1]);
        console.log(JSON.stringify(container, null, 2));
        break;

      case 'start':
        if (!args[1]) {
          console.error('Error: container ID required');
          process.exit(1);
        }
        await client.containers.start(args[1]);
        console.log(JSON.stringify({ success: true, message: `Container ${args[1]} started` }));
        break;

      case 'stop':
        if (!args[1]) {
          console.error('Error: container ID required');
          process.exit(1);
        }
        await client.containers.stop(args[1]);
        console.log(JSON.stringify({ success: true, message: `Container ${args[1]} stopped` }));
        break;

      case 'restart':
        if (!args[1]) {
          console.error('Error: container ID required');
          process.exit(1);
        }
        await client.containers.restart(args[1]);
        console.log(JSON.stringify({ success: true, message: `Container ${args[1]} restarted` }));
        break;

      case 'images':
        const images = await client.images.list();
        console.log(JSON.stringify(images, null, 2));
        break;

      case 'websites':
        const websites = await client.websites.list();
        console.log(JSON.stringify(websites, null, 2));
        break;

      case 'databases':
        const databases = await client.databases.list();
        console.log(JSON.stringify(databases, null, 2));
        break;

      case 'files':
        const path = args[1] || '/';
        const files = await client.files.list(path);
        console.log(JSON.stringify(files, null, 2));
        break;

      case 'system':
        const system = await client.system.getInfo();
        console.log(JSON.stringify(system, null, 2));
        break;

      case 'dashboard':
        const dashboard = await client.dashboard.getBaseInfo();
        console.log(JSON.stringify(dashboard, null, 2));
        break;

      default:
        console.error(`Unknown command: ${command}`);
        console.error('Run without arguments for help');
        process.exit(1);
    }
  } catch (error) {
    console.error(JSON.stringify({ error: true, message: error.message }));
    process.exit(1);
  }
}

main();

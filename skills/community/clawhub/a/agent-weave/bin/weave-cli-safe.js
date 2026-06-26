#!/usr/bin/env node

/**
 * 简化的 weave CLI - 绕过 ESM 兼容问题
 */

const { Loom } = require('../lib/loom-simple');

const args = process.argv.slice(2);
const cmd = args[0];
const subcmd = args[1];

function log(...msg) {
  console.log(...msg);
}

async function main() {
  if (!cmd || cmd === '--help' || cmd === '-h') {
    log('Usage: weave <command> [options]');
    log('');
    log('Commands:');
    log('  loom create-master --name <name>   Create a new Master agent');
    log('  loom list                          List all agents');
    log('  --help                             Show this help');
    return;
  }

  if (cmd === 'loom') {
    if (subcmd === 'list') {
      const loom = new Loom();
      const stats = loom.getStats();
      log('📊 Agent Statistics:');
      log(`  Total: ${stats.total} | Masters: ${stats.masters} | Workers: ${stats.workers}`);
      return;
    }

    if (subcmd === 'create-master') {
      const nameIdx = args.indexOf('--name');
      const name = nameIdx > -1 ? args[nameIdx + 1] : 'master-1';
      
      const loom = new Loom();
      const master = loom.createMaster(name);
      
      log(`✅ Created Master: ${master.name}`);
      log(`   ID: ${master.id}`);
      return;
    }
  }

  log('❌ Unknown command. Use --help for usage.');
  process.exit(1);
}

main().catch(err => {
  console.error('❌ Error:', err.message);
  process.exit(1);
});

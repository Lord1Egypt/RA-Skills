#!/usr/bin/env node

require('../src/load-env')();
const chalk = require('chalk');
const { OpenClawConfigManager, OpenClawMemoryRuntime } = require('../src');

function main() {
  const configManager = new OpenClawConfigManager();
  const memoryRuntime = new OpenClawMemoryRuntime(configManager);
  const payload = memoryRuntime.buildMachineMemorySyncPayload();

  console.log(chalk.blue.bold('🧠 Companion Memory Runtime Check'));
  console.log(
    chalk.gray(`schemaVersion: ${payload.schemaVersion} | agents: ${payload.agents.length}`)
  );

  for (const agent of payload.agents) {
    console.log('');
    console.log(chalk.green(`Agent ${agent.openclawAgentId}`));
    console.log(chalk.gray(`files: ${agent.files.length}`));
    for (const file of agent.files) {
      console.log(`- ${file.filename}`);
    }
  }

  return payload;
}

if (require.main === module) {
  try {
    main();
  } catch (error) {
    console.error(chalk.red(`Memory runtime check failed: ${error.message}`));
    process.exit(1);
  }
}

module.exports = main;

#!/usr/bin/env node

require('../src/load-env')();
const chalk = require('chalk');
const {
  EkybotCompanionApiClient,
  EkybotCompanionStateStore,
} = require('../src');

async function main() {
  const stateStore = new EkybotCompanionStateStore();
  const state = stateStore.load() || {};
  const baseUrl = process.env.EKYBOT_APP_URL || state.baseUrl || 'https://www.ekybot.com';
  const apiClient = new EkybotCompanionApiClient({
    baseUrl,
    machineApiKey: state.machineApiKey,
  });

  console.log(chalk.blue.bold('🔎 Companion API Check'));
  console.log(chalk.gray(`base URL = ${baseUrl}`));
  console.log(chalk.gray(`auth mode = ${apiClient.getAuthMode()}`));
  console.log(
    chalk.gray(
      `registration token present = ${process.env.EKYBOT_COMPANION_REGISTRATION_TOKEN ? 'yes' : 'no'}`
    )
  );
  console.log(chalk.gray(`machine state file = ${stateStore.filePath}`));

  try {
    const result = await apiClient.listMachines();
    console.log(chalk.green('✓ GET /api/companion/machines OK'));
    console.log(
      chalk.gray(
        `machines visible = ${Array.isArray(result?.machines) ? result.machines.length : 0}`
      )
    );
    return {
      success: true,
      baseUrl,
      authMode: apiClient.getAuthMode(),
      machineCount: Array.isArray(result?.machines) ? result.machines.length : 0,
    };
  } catch (error) {
    console.error(chalk.red(`✗ GET /api/companion/machines failed: ${error.message}`));
    process.exit(1);
  }
}

if (require.main === module) {
  main().catch((error) => {
    console.error(chalk.red(`Companion API check failed: ${error.message}`));
    process.exit(1);
  });
}

module.exports = main;

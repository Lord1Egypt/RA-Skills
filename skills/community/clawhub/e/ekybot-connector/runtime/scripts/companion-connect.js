#!/usr/bin/env node

require('../src/load-env')();
const chalk = require('chalk');
const registerCompanion = require('./companion-register');
const syncCompanionInventory = require('./companion-sync');

async function connectCompanion() {
  console.log(chalk.blue.bold('🚀 Companion Connect'));
  console.log(
    chalk.gray(
      'Register the machine, then send an initial heartbeat, inventory, and memory runtime sync.\n'
    )
  );

  const registration = await registerCompanion();
  const syncResult = await syncCompanionInventory();

  console.log(chalk.green('\n✅ Companion onboarding completed'));
  console.log(chalk.gray(`Machine ID: ${registration.machineId}`));
  console.log(chalk.gray(`State file: ${registration.stateFilePath}`));
  console.log(
    chalk.gray(
      `Initial sync: ${syncResult.syncedAgents} agents detected, ${syncResult.memorySyncedAgents} memory payloads synced`
    )
  );
  console.log(chalk.blue('Next step: run "npm run companion:doctor" to verify the setup.'));

  return {
    registration,
    sync: syncResult,
  };
}

if (require.main === module) {
  connectCompanion().catch((error) => {
    console.error(chalk.red(`Companion connect failed: ${error.message}`));
    process.exit(1);
  });
}

module.exports = connectCompanion;

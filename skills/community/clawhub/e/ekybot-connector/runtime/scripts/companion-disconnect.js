#!/usr/bin/env node

require('../src/load-env')();
const chalk = require('chalk');
const inquirer = require('inquirer');
const { EkybotCompanionStateStore } = require('../src');

async function main() {
  console.log(chalk.blue.bold('🔌 Companion Disconnect'));

  const stateStore = new EkybotCompanionStateStore();
  const state = stateStore.load();

  if (!state?.machineId) {
    console.log(chalk.yellow('No companion machine is currently registered.'));
    return;
  }

  const nonInteractive = process.env.CI === 'true' || process.env.EKYBOT_COMPANION_FORCE === '1';
  let confirmed = nonInteractive;

  if (!nonInteractive) {
    const answer = await inquirer.prompt([
      {
        type: 'confirm',
        name: 'confirmed',
        message: `Disconnect machine "${state.machineName || state.machineId}" from local Companion state?`,
        default: false,
      },
    ]);
    confirmed = answer.confirmed;
  }

  if (!confirmed) {
    console.log(chalk.gray('Disconnect cancelled.'));
    return;
  }

  stateStore.clear();
  console.log(chalk.green(`Disconnected local Companion state for ${state.machineName || state.machineId}.`));
  console.log(chalk.gray(`State file cleared: ${stateStore.filePath}`));
  console.log(chalk.gray('The machine identity file was kept to preserve the fingerprint.'));
}

if (require.main === module) {
  main().catch((error) => {
    console.error(chalk.red(`Companion disconnect failed: ${error.message}`));
    process.exit(1);
  });
}

module.exports = main;

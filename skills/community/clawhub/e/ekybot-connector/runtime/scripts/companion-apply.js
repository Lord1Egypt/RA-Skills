#!/usr/bin/env node

require('../src/load-env')();
const chalk = require('chalk');
const {
  EkybotCompanionApiClient,
  EkybotCompanionExecutor,
  EkybotCompanionStateStore,
  OpenClawConfigManager,
} = require('../src');

async function applyCompanionOperations() {
  console.log(chalk.blue.bold('🛠️  Ekybot Companion Apply'));

  const stateStore = new EkybotCompanionStateStore();
  const state = stateStore.load();

  if (!state?.machineId || !state?.machineApiKey) {
    console.error(chalk.red('❌ No companion machine registered'));
    console.error(chalk.yellow('Run "npm run companion:register" first.'));
    process.exit(1);
  }

  const apiClient = new EkybotCompanionApiClient({
    baseUrl: state.baseUrl,
    machineApiKey: state.machineApiKey,
  });
  const configManager = new OpenClawConfigManager();
  const executor = new EkybotCompanionExecutor(apiClient, configManager, stateStore);

  const result = await executor.applyDesiredState(state.machineId);

  console.log(
    chalk.green(
      `✓ Apply completed (${result.appliedOperationIds.length}/${result.pendingOperations.length} operations applied)`
    )
  );
  if (result.implicitSyncApplied) {
    console.log(chalk.green('✓ Desired state changes were synced to the managed fragment'));
  }
  if (result.failedOperationCount > 0) {
    console.log(chalk.yellow(`! ${result.failedOperationCount} operations need attention`));
  }
  console.log(
    chalk.gray(
      `Managed agents in desired state: ${(result.desiredState?.agents || []).length}`
    )
  );
}

if (require.main === module) {
  applyCompanionOperations().catch((error) => {
    console.error(chalk.red(`Companion apply failed: ${error.message}`));
    process.exit(1);
  });
}

module.exports = applyCompanionOperations;

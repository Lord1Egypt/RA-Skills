#!/usr/bin/env node

require('../src/load-env')();
const fs = require('fs');
const chalk = require('chalk');
const {
  EkybotCompanionApiClient,
  EkybotCompanionStateStore,
  OpenClawConfigManager,
  OpenClawInventoryCollector,
  OpenClawMemoryRuntime,
} = require('../src');

function printCheck(ok, label, detail) {
  const icon = ok ? chalk.green('✓') : chalk.red('✗');
  const title = ok ? chalk.green(label) : chalk.red(label);
  console.log(`${icon} ${title}${detail ? chalk.gray(` — ${detail}`) : ''}`);
}

async function main() {
  console.log(chalk.blue.bold('🩺 Companion Doctor'));

  const stateStore = new EkybotCompanionStateStore();
  const state = stateStore.load() || {};
  const configManager = new OpenClawConfigManager();
  const inventoryCollector = new OpenClawInventoryCollector(configManager, {
    machineName: state.machineName,
  });
  const memoryRuntime = new OpenClawMemoryRuntime(configManager);

  const checks = [];
  const baseUrl = process.env.EKYBOT_APP_URL || state.baseUrl || 'https://www.ekybot.com';

  checks.push({
    ok: Boolean(state.machineId && state.machineApiKey),
    label: 'Companion machine state',
    detail: state.machineId ? `machineId=${state.machineId}` : 'run npm run companion:connect',
  });

  checks.push({
    ok: fs.existsSync(configManager.configPath),
    label: 'OpenClaw config file',
    detail: configManager.configPath,
  });

  const inventory = inventoryCollector.collect();
  checks.push({
    ok: inventory.validation.configExists && inventory.validation.configValid,
    label: 'OpenClaw config validity',
    detail: inventory.validation.configValid ? `${inventory.agents.length} agent(s) detected` : 'config invalid or missing',
  });

  const memoryPayload = memoryRuntime.buildMachineMemorySyncPayload();
  const memoryFileCount = memoryPayload.agents.reduce((sum, agent) => sum + agent.files.length, 0);
  checks.push({
    ok: memoryPayload.agents.length > 0 && memoryFileCount > 0,
    label: 'Memory runtime artifacts',
    detail: `${memoryPayload.agents.length} agent(s), ${memoryFileCount} file(s)`,
  });

  let apiCheck = null;
  if (state.machineApiKey) {
    const apiClient = new EkybotCompanionApiClient({
      baseUrl,
      machineApiKey: state.machineApiKey,
    });
    try {
      const result = await apiClient.listMachines();
      apiCheck = {
        ok: true,
        label: 'Companion API access',
        detail: `${Array.isArray(result?.machines) ? result.machines.length : 0} machine(s) visible`,
      };
    } catch (error) {
      apiCheck = {
        ok: false,
        label: 'Companion API access',
        detail: error.message,
      };
    }
  } else {
    apiCheck = {
      ok: false,
      label: 'Companion API access',
      detail: 'missing machineApiKey in state file',
    };
  }

  checks.push(apiCheck);

  console.log(chalk.gray(`base URL = ${baseUrl}`));
  console.log(chalk.gray(`state file = ${stateStore.filePath}`));
  console.log(chalk.gray(`identity file = ${stateStore.identityFilePath}`));
  console.log('');

  checks.forEach((check) => printCheck(check.ok, check.label, check.detail));

  const failedChecks = checks.filter((check) => !check.ok);
  if (failedChecks.length > 0) {
    console.log('');
    console.log(chalk.yellow('Recommended next steps:'));
    if (!state.machineId || !state.machineApiKey) {
      console.log(chalk.yellow('- Run "npm run companion:connect" to register this machine.'));
    }
    if (!fs.existsSync(configManager.configPath)) {
      console.log(chalk.yellow(`- Verify OPENCLAW_CONFIG_PATH or create the config at ${configManager.configPath}.`));
    }
    if (apiCheck && !apiCheck.ok) {
      console.log(chalk.yellow('- Run "npm run companion:api-check" to inspect the API auth details.'));
    }
    process.exit(1);
  }

  console.log('');
  console.log(chalk.green('Companion doctor passed.'));
}

if (require.main === module) {
  main().catch((error) => {
    console.error(chalk.red(`Companion doctor failed: ${error.message}`));
    process.exit(1);
  });
}

module.exports = main;

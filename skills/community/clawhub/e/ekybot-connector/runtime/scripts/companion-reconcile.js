#!/usr/bin/env node

require('../src/load-env')();
const chalk = require('chalk');
const crypto = require('crypto');
const {
  EkybotCompanionApiClient,
  EkybotCompanionExecutor,
  EkybotCompanionStateStore,
  OpenClawConfigManager,
  OpenClawGatewayClient,
  OpenClawInventoryCollector,
  EkybotCompanionRelayProcessor,
} = require('../src');
const { buildCompanionRuntimeState } = require('../src/companion-runtime-state');

const DESIRED_STATE_CACHE_MS = 10_000;
const INVENTORY_MIN_INTERVAL_MS = 5 * 60 * 1000;

function hashInventoryPayload(inventory) {
  const normalizedInventory = {
    machineId: inventory.machineId,
    machineFingerprint: inventory.machineFingerprint || null,
    configHash: inventory.configHash || null,
    rootConfigPath: inventory.rootConfigPath || null,
    managedFragmentPaths: Array.isArray(inventory.managedFragmentPaths)
      ? inventory.managedFragmentPaths
      : [],
    agents: Array.isArray(inventory.agents) ? inventory.agents : [],
  };

  return crypto.createHash('sha256').update(JSON.stringify(normalizedInventory)).digest('hex');
}

function shouldUploadInventory(state, fingerprint, { force = false } = {}) {
  if (force) {
    return true;
  }

  if (!state?.lastInventoryUploadedAt || !state?.lastInventoryPayloadHash) {
    return true;
  }

  if (state.lastInventoryPayloadHash !== fingerprint) {
    return true;
  }

  const lastUploadedAt = Date.parse(state.lastInventoryUploadedAt);
  if (!Number.isFinite(lastUploadedAt)) {
    return true;
  }

  return Date.now() - lastUploadedAt >= INVENTORY_MIN_INTERVAL_MS;
}

async function reconcileCompanionState() {
  console.log(chalk.blue.bold('🔁 Ekybot Companion Reconcile'));

  const stateStore = new EkybotCompanionStateStore();
  const state = stateStore.load();

  if (!state?.machineId || !state?.machineApiKey) {
    console.error(chalk.red('❌ No companion machine registered'));
    console.error(chalk.yellow('Run "npm run companion:register" first.'));
    process.exit(1);
  }

  if (state.machineFingerprint) {
    process.env.EKYBOT_MACHINE_FINGERPRINT = state.machineFingerprint;
  }

  const startedAt = new Date().toISOString();
  stateStore.merge({
    lastReconcileStartedAt: startedAt,
  });

  const apiClient = new EkybotCompanionApiClient({
    baseUrl: state.baseUrl,
    machineApiKey: state.machineApiKey,
  });
  const configManager = new OpenClawConfigManager();
  const inventoryCollector = new OpenClawInventoryCollector(configManager, {
    machineName: state.machineName,
  });
  const executor = new EkybotCompanionExecutor(apiClient, configManager, stateStore);
  const relayProcessor = new EkybotCompanionRelayProcessor(apiClient, new OpenClawGatewayClient(), {
    stateStore,
    inventoryCollector,
    machineId: state.machineId,
  });

  const buildHeartbeat = (runtimeState, pendingOperationCount) => {
    const heartbeat = inventoryCollector.toHeartbeatPayload(state.machineId);
    heartbeat.pendingOperationCount = pendingOperationCount;
    heartbeat.runtimeState = buildCompanionRuntimeState(runtimeState);
    return heartbeat;
  };

  const sendInventorySnapshot = async (options = {}) => {
    const currentState = stateStore.load() || state;
    const inventory = inventoryCollector.toMachineInventoryPayload(state.machineId);
    const fingerprint = hashInventoryPayload(inventory);

    if (!shouldUploadInventory(currentState, fingerprint, options)) {
      return {
        inventory,
        fingerprint,
        uploaded: false,
      };
    }

    await apiClient.uploadInventory(state.machineId, inventory);
    const uploadedAt = new Date().toISOString();
    stateStore.merge({
      lastInventoryUploadedAt: uploadedAt,
      lastInventoryHash: inventory.configHash,
      lastInventoryPayloadHash: fingerprint,
    });

    return {
      inventory,
      fingerprint,
      uploaded: true,
    };
  };

  const initialDesiredState = await apiClient.fetchDesiredStateCached(state.machineId, {
    maxAgeMs: DESIRED_STATE_CACHE_MS,
  });
  const runtimeBefore = stateStore.load() || state;
  await apiClient.sendHeartbeat(
    state.machineId,
    buildHeartbeat(
      {
        activeRequests: runtimeBefore.activeRequests,
        lastDesiredSyncAt: runtimeBefore.lastDesiredSyncAt,
        lastInventoryUploadedAt: runtimeBefore.lastInventoryUploadedAt,
        lastApplyStartedAt: runtimeBefore.lastApplyStartedAt,
        lastApplyCompletedAt: runtimeBefore.lastApplyCompletedAt,
        lastReconciledAt: runtimeBefore.lastReconciledAt,
        lastAppliedDesiredConfigVersion: runtimeBefore.lastAppliedDesiredConfigVersion,
        lastAppliedManagedFragmentPath: runtimeBefore.lastAppliedManagedFragmentPath,
        lastAppliedManagedFragmentHash: runtimeBefore.lastAppliedManagedFragmentHash,
        driftDetected: runtimeBefore.driftDetected ?? false,
        driftReason: runtimeBefore.driftReason,
      },
      (initialDesiredState.pendingOperations || []).length
    )
  );

  const firstInventoryResult = await sendInventorySnapshot();
  stateStore.merge({
    lastDesiredSyncAt: startedAt,
    ...(firstInventoryResult.uploaded
      ? {}
      : {
          lastInventoryHash: firstInventoryResult.inventory.configHash,
          lastInventoryPayloadHash: firstInventoryResult.fingerprint,
        }),
  });

  const applyResult = await executor.applyDesiredState(state.machineId, {
    prefetchedDesiredState: initialDesiredState,
  });

  const secondInventoryResult = await sendInventorySnapshot({
    force: applyResult.implicitSyncApplied || applyResult.appliedOperationIds.length > 0,
  });
  const finishedAt = new Date().toISOString();
  const shouldRefreshDesiredState =
    applyResult.implicitSyncApplied ||
    applyResult.appliedOperationIds.length > 0 ||
    (initialDesiredState.pendingOperations || []).length > 0;
  const finalDesiredState = shouldRefreshDesiredState
    ? await apiClient.fetchDesiredStateCached(state.machineId, {
        forceRefresh: true,
      })
    : initialDesiredState;
  const finalPendingOperationCount = (finalDesiredState.pendingOperations || []).filter(
    (operation) => operation.status === 'pending' || operation.status === 'in_progress'
  ).length;
  const driftDetected =
    finalPendingOperationCount > 0 || applyResult.failedOperationCount > 0;
  const driftReason = driftDetected
    ? applyResult.failedOperationCount > 0
      ? 'Some operations failed during reconcile'
      : 'Pending operations remain after reconcile'
    : null;

  stateStore.merge({
    lastDesiredSyncAt: finishedAt,
    ...(secondInventoryResult.uploaded
      ? {}
      : {
          lastInventoryHash: secondInventoryResult.inventory.configHash,
          lastInventoryPayloadHash: secondInventoryResult.fingerprint,
        }),
    lastReconciledAt: finishedAt,
    driftDetected,
    driftReason,
  });

  const finalState = stateStore.load() || state;
  await apiClient.sendHeartbeat(
    state.machineId,
    buildHeartbeat(
      {
        activeRequests: finalState.activeRequests,
        lastDesiredSyncAt: finalState.lastDesiredSyncAt,
        lastInventoryUploadedAt: finalState.lastInventoryUploadedAt,
        lastApplyStartedAt: finalState.lastApplyStartedAt,
        lastApplyCompletedAt: finalState.lastApplyCompletedAt,
        lastReconciledAt: finalState.lastReconciledAt,
        lastAppliedDesiredConfigVersion: finalState.lastAppliedDesiredConfigVersion,
        lastAppliedManagedFragmentPath: finalState.lastAppliedManagedFragmentPath,
        lastAppliedManagedFragmentHash: finalState.lastAppliedManagedFragmentHash,
        driftDetected: finalState.driftDetected ?? false,
        driftReason: finalState.driftReason,
      },
      finalPendingOperationCount
    )
  );

  const relayResult = await relayProcessor.processPendingRelays(state.machineId);

  console.log(
    chalk.green(
      `✓ Reconcile completed (${applyResult.appliedOperationIds.length}/${applyResult.pendingOperations.length} operations applied)`
    )
  );
  if (applyResult.implicitSyncApplied) {
    console.log(chalk.green('✓ Desired state changes were synced to the managed fragment'));
  }
  console.log(chalk.gray(`Managed agents written: ${(applyResult.desiredState?.agents || []).length}`));
  console.log(
    chalk.gray(
      `Inventory uploads: first=${firstInventoryResult.uploaded ? 'sent' : 'skipped'} second=${secondInventoryResult.uploaded ? 'sent' : 'skipped'}`
    )
  );
  console.log(chalk.gray(`Pending operations remaining: ${finalPendingOperationCount}`));
  if (relayResult.fetched > 0) {
    console.log(
      chalk.gray(
        `Relay notifications: ${relayResult.delivered}/${relayResult.fetched} delivered, ${relayResult.replied} replies published${relayResult.failed > 0 ? `, ${relayResult.failed} failed` : ''}`
      )
    );
  }
  console.log(
    driftDetected
      ? chalk.yellow(`Drift detected: ${driftReason}`)
      : chalk.green('Machine is in sync with desired state')
  );
}

if (require.main === module) {
  reconcileCompanionState().catch((error) => {
    console.error(chalk.red(`Companion reconcile failed: ${error.message}`));
    process.exit(1);
  });
}

module.exports = reconcileCompanionState;

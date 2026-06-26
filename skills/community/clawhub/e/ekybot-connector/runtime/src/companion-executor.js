const crypto = require('crypto');
const chalk = require('chalk');

class EkybotCompanionExecutor {
  constructor(apiClient, configManager, stateStore, options = {}) {
    this.apiClient = apiClient;
    this.configManager = configManager;
    this.stateStore = stateStore;
    this.logger = options.logger || console;
  }

  hashString(value) {
    return crypto.createHash('sha256').update(value).digest('hex');
  }

  async applyDesiredState(machineId, options = {}) {
    const applyStartedAt = new Date().toISOString();
    this.stateStore.merge({
      lastApplyStartedAt: applyStartedAt,
    });

    const response = options.prefetchedDesiredState || (await this.apiClient.fetchDesiredState(machineId));
    const desiredState = response?.desiredState;
    const pendingOperations = response?.pendingOperations || [];

    if (!desiredState) {
      throw new Error('Missing desired state payload');
    }

    const persistedState = this.stateStore.load() || {};
    const needsImplicitManagedFragmentSync =
      desiredState.desiredConfigVersion !==
      (persistedState.lastAppliedDesiredConfigVersion ?? null);

    const applied = [];
    let implicitSyncApplied = false;

    if (needsImplicitManagedFragmentSync && pendingOperations.length === 0) {
      const includeInfo = this.configManager.ensureManagedInclude(
        desiredState.managedFragmentPath
      );
      const fragmentInfo = this.configManager.writeManagedFragment(desiredState);

      this.stateStore.merge({
        lastAppliedDesiredConfigVersion: desiredState.desiredConfigVersion,
        lastAppliedManagedFragmentPath: fragmentInfo.fragmentPath,
        lastAppliedManagedFragmentHash: fragmentInfo.fragmentHash,
      });

      this.logger.log(
        chalk.green(
          `✓ desired state synced (${desiredState.agents.length} managed agents written)`
        )
      );

      implicitSyncApplied = true;

      if (includeInfo.updated) {
        this.logger.log(chalk.green('✓ managed include bootstrapped'));
      }
    }

    for (const operation of pendingOperations) {
      try {
        await this.applyOperation(machineId, operation, desiredState);
        applied.push(operation.id);
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Unknown execution error';
        await this.apiClient.updateOperation(machineId, operation.id, {
          status: 'failed',
          error: message,
          result: {
            attemptedAt: new Date().toISOString(),
          },
        });
        this.logger.error(chalk.red(`✗ Operation ${operation.type} failed: ${message}`));
      }
    }

    const applyCompletedAt = new Date().toISOString();
    const failedOperationCount = pendingOperations.length - applied.length;
    const nextDriftDetected =
      failedOperationCount > 0 ||
      pendingOperations.some((operation) => !applied.includes(operation.id));

    this.stateStore.merge({
      lastApplyCompletedAt: applyCompletedAt,
      lastDesiredSyncAt: applyCompletedAt,
      driftDetected: nextDriftDetected,
      driftReason: nextDriftDetected
        ? failedOperationCount > 0
          ? 'Some pending operations failed during local apply'
          : 'Pending operations remain after local apply'
        : null,
    });

    return {
      desiredState,
      pendingOperations,
      appliedOperationIds: applied,
      failedOperationCount,
      applyStartedAt,
      applyCompletedAt,
      implicitSyncApplied,
    };
  }

  async applyOperation(machineId, operation, desiredState) {
    const appliesManagedState = new Set([
      'bootstrap_include',
      'import_agent',
      'create_agent',
      'update_agent_model',
      'update_agent_bindings',
      'update_workspace_templates',
      'archive_agent',
    ]);

    if (operation.type === 'scan_inventory') {
      await this.apiClient.updateOperation(machineId, operation.id, {
        status: 'applied',
        result: {
          appliedAt: new Date().toISOString(),
          action: 'inventory_rescan_requested',
        },
      });
      this.logger.log(chalk.green('✓ scan_inventory acknowledged'));
      return;
    }

    if (appliesManagedState.has(operation.type)) {
      const includeInfo = this.configManager.ensureManagedInclude(
        desiredState.managedFragmentPath
      );
      const fragmentInfo = this.configManager.writeManagedFragment(desiredState);

      const persistedState = this.stateStore.load() || {};
      this.stateStore.save({
        ...persistedState,
        lastAppliedDesiredConfigVersion: desiredState.desiredConfigVersion,
        lastAppliedManagedFragmentPath: fragmentInfo.fragmentPath,
        lastAppliedManagedFragmentHash: fragmentInfo.fragmentHash,
      });

      await this.apiClient.updateOperation(machineId, operation.id, {
        status: 'applied',
        result: {
          appliedAt: new Date().toISOString(),
          desiredConfigVersion: desiredState.desiredConfigVersion,
          includeUpdated: includeInfo.updated,
          fragmentPath: fragmentInfo.fragmentPath,
          fragmentHash: fragmentInfo.fragmentHash,
          managedAgentCount: desiredState.agents.length,
        },
      });

      this.logger.log(
        chalk.green(
          `✓ ${operation.type} applied (${desiredState.agents.length} managed agents written)`
        )
      );
      return;
    }

    if (operation.type === 'delete_agent') {
      const payload = operation.payload || {};
      const removeInfo = this.configManager.removeAgentFromConfig({
        openclawAgentId: payload.openclawAgentId,
        workspacePath: payload.workspacePath,
        name: payload.name,
      });
      const preserveWorkspace = payload.preserveWorkspace === true;
      const workspaceInfo = preserveWorkspace
        ? {
            deleted: false,
            preserved: true,
            reason: 'preserve_workspace_requested',
            workspacePath: payload.workspacePath || null,
          }
        : this.configManager.deleteWorkspace(payload.workspacePath);
      const includeInfo = this.configManager.ensureManagedInclude(
        desiredState.managedFragmentPath
      );
      const fragmentInfo = this.configManager.writeManagedFragment(desiredState);
      const managedFragmentRemoveInfo = this.configManager.removeAgentFromManagedFragment({
        openclawAgentId: payload.openclawAgentId,
        workspacePath: payload.workspacePath,
        name: payload.name,
      });

      const persistedState = this.stateStore.load() || {};
      this.stateStore.save({
        ...persistedState,
        lastAppliedDesiredConfigVersion: desiredState.desiredConfigVersion,
        lastAppliedManagedFragmentPath: fragmentInfo.fragmentPath,
        lastAppliedManagedFragmentHash:
          managedFragmentRemoveInfo.fragmentHash || fragmentInfo.fragmentHash,
      });

      await this.apiClient.updateOperation(machineId, operation.id, {
        status: 'applied',
        result: {
          appliedAt: new Date().toISOString(),
          desiredConfigVersion: desiredState.desiredConfigVersion,
          includeUpdated: includeInfo.updated,
          fragmentPath: fragmentInfo.fragmentPath,
          fragmentHash: fragmentInfo.fragmentHash,
          managedAgentCount: desiredState.agents.length,
          removedFromConfig: removeInfo.updated,
          removedFromManagedFragment: managedFragmentRemoveInfo.updated,
          workspaceDeleted: workspaceInfo.deleted,
          workspacePreserved: workspaceInfo.preserved === true,
          workspaceDeleteReason: workspaceInfo.reason || null,
          workspacePath: workspaceInfo.workspacePath || payload.workspacePath || null,
        },
      });

      this.logger.log(
        chalk.green(
          `✓ delete_agent applied (${payload.openclawAgentId || payload.name || 'unknown'} removed${preserveWorkspace ? ', workspace preserved' : ''})`
        )
      );
      return;
    }

    await this.apiClient.updateOperation(machineId, operation.id, {
      status: 'manual_action_required',
      error: `Unsupported local operation type: ${operation.type}`,
    });
    this.logger.log(chalk.yellow(`! Unsupported operation ${operation.type}`));
  }
}

module.exports = EkybotCompanionExecutor;

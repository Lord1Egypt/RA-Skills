import { manifest } from "../core/contracts.js";
import { ensureCondition, toStepRollbackError } from "../core/errors.js";
import { nowIso } from "../core/utils.js";

import { requireOwnedCheckpoint } from "./session-support.js";

export async function executeRollback({
  config,
  host,
  services,
  agentId,
  sessionId,
  checkpointId,
  restoreWorkspace = false,
  logger
}) {
  return services.lockManager.withLock(agentId, sessionId, async () => {
    const checkpoint = await requireOwnedCheckpoint(services, {
      agentId,
      sessionId,
      checkpointId
    });
    const currentState = await services.runtimeCursorManager.ensure(agentId, sessionId);

    ensureCondition(
      !currentState.rollbackInProgress,
      "ROLLBACK_IN_PROGRESS",
      `Rollback is already running for session '${sessionId}'.`,
      { agentId, sessionId }
    );

    await services.runtimeCursorManager.setRollbackState(agentId, sessionId, true);

    let rollbackId = null;

    try {
      if (config.stopRunBeforeRollback && currentState.currentRunId) {
        const stopResult = await host.stopRun({
          agentId,
          sessionId,
          runId: currentState.currentRunId,
          checkpointId
        });
        const stopped = stopResult === undefined ? true : stopResult === true || stopResult.stopped !== false;

        ensureCondition(
          stopped,
          "RUN_STOP_FAILED",
          `Failed to stop run '${currentState.currentRunId}' before rollback.`,
          { agentId, sessionId, checkpointId, runId: currentState.currentRunId }
        );
      }

      await services.checkpointManager.restore(checkpointId, {
        restoreWorkspace: Boolean(restoreWorkspace),
        restoreRuntimeState: true
      });

      await services.runtimeCursorManager.applyRollback(agentId, sessionId, {
        entryId: checkpoint.entryId,
        checkpointId
      });

      rollbackId = await services.sequenceStore.next("rb");
      await services.reportWriter.save({
        rollbackId,
        agentId,
        sessionId,
        checkpointId,
        targetEntryId: checkpoint.entryId,
        triggeredAt: nowIso(),
        result: "success",
        message: restoreWorkspace ? "rollback completed" : "rollback completed without workspace restore",
        restoredWorkspace: Boolean(restoreWorkspace)
      });

      logger.info?.(
        `[${manifest.id}] rollback completed agent='${agentId}' session='${sessionId}' checkpoint='${checkpointId}' rollback='${rollbackId}'`
      );

      return {
        rollbackId,
        agentId,
        sessionId,
        checkpointId,
        targetEntryId: checkpoint.entryId,
        result: "success",
        restoredWorkspace: Boolean(restoreWorkspace),
        awaitingContinue: false,
        activeHeadEntryId: checkpoint.entryId
      };
    } catch (error) {
      const normalizedError = toStepRollbackError(error, "SNAPSHOT_RESTORE_FAILED", {
        agentId,
        sessionId,
        checkpointId
      });

      logger.error?.(
        `[${manifest.id}] rollback failed agent='${agentId}' session='${sessionId}' checkpoint='${checkpointId}': ${normalizedError.message}`
      );

      rollbackId = rollbackId ?? (await services.sequenceStore.next("rb"));
      await services.reportWriter.save({
        rollbackId,
        agentId,
        sessionId,
        checkpointId,
        targetEntryId: checkpoint?.entryId ?? null,
        triggeredAt: nowIso(),
        result: "failed",
        message: normalizedError.message,
        restoredWorkspace: Boolean(restoreWorkspace)
      });

      throw normalizedError;
    } finally {
      await services.runtimeCursorManager.setRollbackState(agentId, sessionId, false);
    }
  });
}

import crypto from "node:crypto";

import { ensureCondition } from "../core/errors.js";
import { nowIso } from "../core/utils.js";

export async function executeCheckout({
  host,
  services,
  agentId,
  sourceSessionId,
  sourceEntryId,
  continueAfterCheckout = false,
  prompt
}) {
  return services.lockManager.withLock(agentId, sourceSessionId, async () => {
    const checkpoints = await services.checkpointManager.list(agentId, sourceSessionId);
    const checkpoint = checkpoints.find((item) => item.entryId === sourceEntryId);

    ensureCondition(
      checkpoint,
      "ENTRY_NOT_FOUND",
      `Entry '${sourceEntryId}' was not found in session '${sourceSessionId}'.`,
      { agentId, sourceSessionId, sourceEntryId }
    );
    ensureCondition(
      checkpoint.status === "ready" || checkpoint.status === "restored",
      "CHECKOUT_NOT_SUPPORTED",
      `Entry '${sourceEntryId}' is not available for checkout.`,
      { agentId, sourceSessionId, sourceEntryId, checkpointId: checkpoint.checkpointId }
    );

    await services.checkpointManager.restore(checkpoint.checkpointId, {
      restoreWorkspace: true,
      restoreRuntimeState: false
    });

    const branchId = await services.sequenceStore.next("br");
    const createdSession = await host.createSession({
      agentId,
      sourceSessionId,
      sourceEntryId,
      checkpointId: checkpoint.checkpointId,
      branchId,
      purpose: "checkout"
    });

    const provisionalSessionId = createdSession?.sessionId ?? crypto.randomUUID();
    const provisionalSessionKey = createdSession?.sessionKey ?? null;

    let continued = false;
    let usedPrompt = false;
    let resolvedSessionId = provisionalSessionId;
    let resolvedSessionKey = provisionalSessionKey;

    if (continueAfterCheckout) {
      const runResult = await host.startContinueRun({
        agentId,
        sessionId: provisionalSessionId,
        sessionKey: provisionalSessionKey,
        entryId: sourceEntryId,
        prompt,
        checkpointId: checkpoint.checkpointId,
        sourceSessionId,
        sourceEntryId,
        branchId,
        label: createdSession?.label
      });
      const started = runResult === undefined ? true : runResult === true || runResult.started !== false;

      ensureCondition(
        started,
        "CONTINUE_START_FAILED",
        `Failed to continue newly checked out session '${provisionalSessionId}'.`,
        { agentId, sourceSessionId, newSessionId: provisionalSessionId, sourceEntryId }
      );

      resolvedSessionId = runResult?.sessionId ?? provisionalSessionId;
      resolvedSessionKey = runResult?.sessionKey ?? provisionalSessionKey ?? null;
      await services.runtimeCursorManager.replace(agentId, resolvedSessionId, {
        activeHeadEntryId: sourceEntryId,
        currentRunId: runResult?.runId ?? null,
        rollbackInProgress: false,
        awaitingContinue: false,
        lastRollbackCheckpointId: checkpoint.checkpointId
      });
      await services.runtimeCursorManager.applyContinue(agentId, resolvedSessionId, {
        prompt,
        runId: runResult?.runId ?? null
      });
      continued = true;
      usedPrompt = Boolean(prompt);
    } else {
      await services.runtimeCursorManager.replace(agentId, resolvedSessionId, {
        activeHeadEntryId: sourceEntryId,
        currentRunId: null,
        rollbackInProgress: false,
        awaitingContinue: false,
        lastRollbackCheckpointId: checkpoint.checkpointId
      });
    }

    await services.registry.saveBranch({
      branchId,
      branchType: "session",
      sourceAgentId: agentId,
      sourceSessionId,
      sourceEntryId,
      sourceCheckpointId: checkpoint.checkpointId,
      newAgentId: agentId,
      newSessionId: resolvedSessionId,
      newSessionKey: resolvedSessionKey,
      createdAt: nowIso(),
      reason: continueAfterCheckout ? "checkout-continue" : "checkout"
    });

    return {
      branchId,
      sourceSessionId,
      sourceEntryId,
      newSessionId: resolvedSessionId,
      newSessionKey: resolvedSessionKey,
      continued,
      usedPrompt
    };
  });
}

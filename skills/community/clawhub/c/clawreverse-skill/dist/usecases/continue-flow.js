import crypto from "node:crypto";

import { manifest } from "../core/contracts.js";
import { StepRollbackError, ensureCondition } from "../core/errors.js";
import { nowIso } from "../core/utils.js";

import { requireOwnedCheckpoint } from "./session-support.js";

export async function executeContinue({
  config,
  host,
  services,
  agentId,
  sessionId,
  checkpointId,
  prompt,
  newAgentId,
  cloneAuth,
  log = false,
  logger
}) {
  ensureCondition(
    checkpointId,
    "CHECKPOINT_NOT_FOUND",
    "checkpointId is required to continue from a checkpoint.",
    { agentId, sessionId }
  );
  ensureCondition(
    typeof prompt === "string" && prompt.trim(),
    "ERR_PROMPT_REQUIRED",
    "continue requires a non-empty prompt.",
    { agentId, sessionId, checkpointId }
  );

  if (!config.allowContinuePrompt) {
    throw new StepRollbackError(
      "CONTINUE_START_FAILED",
      "Continue prompt is disabled by plugin configuration.",
      { agentId, sessionId, checkpointId }
    );
  }

  await services.runtimeCursorManager.ensure(agentId, sessionId);
  const checkpoint = await requireOwnedCheckpoint(services, {
    agentId,
    sessionId,
    checkpointId
  });
  const branchId = await services.sequenceStore.next("br");
  const forkResult = await host.forkContinue({
    sourceAgentId: agentId,
    sourceSessionId: sessionId,
    sourceEntryId: checkpoint.entryId,
    checkpoint,
    prompt,
    newAgentId,
    cloneAuth,
    branchId,
    log
  });

  const started = forkResult === undefined ? true : forkResult === true || forkResult.started !== false;

  ensureCondition(
    started,
    "CONTINUE_START_FAILED",
    `Failed to fork a new agent from checkpoint '${checkpointId}'.`,
    { agentId, sessionId, checkpointId, newAgentId }
  );

  const resolvedAgentId = forkResult?.newAgentId ?? newAgentId ?? `${agentId}-cp-${branchId.slice(-4)}`;
  const resolvedSessionId = forkResult?.newSessionId ?? crypto.randomUUID();
  const resolvedSessionKey = forkResult?.newSessionKey ?? null;
  const resolvedWorkspacePath = forkResult?.newWorkspacePath ?? null;
  const resolvedAgentDir = forkResult?.newAgentDir ?? null;
  const resolvedLogFilePath = forkResult?.logFilePath ?? null;
  const createdNewAgent = forkResult?.createdNewAgent ?? true;

  await services.registry.saveBranch({
    branchId,
    branchType: "agent",
    sourceAgentId: agentId,
    sourceSessionId: sessionId,
    sourceEntryId: checkpoint.entryId,
    sourceCheckpointId: checkpoint.checkpointId,
    newAgentId: resolvedAgentId,
    newWorkspacePath: resolvedWorkspacePath,
    newAgentDir: resolvedAgentDir,
    logFilePath: resolvedLogFilePath,
    newSessionId: resolvedSessionId,
    newSessionKey: resolvedSessionKey,
    prompt,
    createdAt: nowIso(),
    reason: "continue",
    createdNewAgent
  });
  await services.runtimeCursorManager.replace(resolvedAgentId, resolvedSessionId, {
    activeHeadEntryId: checkpoint.entryId,
    currentRunId: forkResult?.runId ?? null,
    rollbackInProgress: false,
    awaitingContinue: false,
    lastRollbackCheckpointId: checkpoint.checkpointId
  });
  await services.runtimeCursorManager.update(agentId, sessionId, (currentState) => {
    currentState.awaitingContinue = false;
    currentState.rollbackInProgress = false;
    currentState.lastContinuePrompt = prompt;
    currentState.currentRunId = null;
    currentState.lastContinuedBranchId = branchId;
    currentState.lastContinueSessionId = resolvedSessionId;
    currentState.lastContinueSessionKey = resolvedSessionKey ?? undefined;
    return currentState;
  });

  logger.info?.(
    `[${manifest.id}] continue forked parentAgent='${agentId}' session='${sessionId}' branch='${branchId}' newAgent='${resolvedAgentId}' newSession='${resolvedSessionId}'`
  );

  return {
    ok: true,
    parentAgentId: agentId,
    parentSessionId: sessionId,
    sourceEntryId: checkpoint.entryId,
    checkpointId: checkpoint.checkpointId,
    branchId,
    newAgentId: resolvedAgentId,
    newWorkspacePath: resolvedWorkspacePath,
    newAgentDir: resolvedAgentDir,
    logFilePath: resolvedLogFilePath,
    newSessionId: resolvedSessionId,
    newSessionKey: resolvedSessionKey,
    createdNewAgent,
    continued: true,
    started: forkResult?.started !== false,
    usedPrompt: true
  };
}

import { ensureCondition } from "../core/errors.js";

export function assertSessionRequest(agentId, sessionId) {
  ensureCondition(agentId, "SESSION_NOT_FOUND", "agentId is required.");
  ensureCondition(sessionId, "SESSION_NOT_FOUND", "sessionId is required.");
}

export function toRollbackStatus(agentId, sessionId, state) {
  return {
    agentId,
    sessionId,
    rollbackInProgress: state?.rollbackInProgress ?? false,
    awaitingContinue: state?.awaitingContinue ?? false,
    activeHeadEntryId: state?.activeHeadEntryId ?? null,
    lastRollbackCheckpointId: state?.lastRollbackCheckpointId ?? undefined
  };
}

export async function requireOwnedCheckpoint(services, { agentId, sessionId, checkpointId }) {
  const checkpoint = checkpointId === "latest"
    ? (await services.checkpointManager.list(agentId, sessionId)).at(-1) ?? null
    : await services.checkpointManager.get(checkpointId);

  ensureCondition(
    checkpoint,
    "CHECKPOINT_NOT_FOUND",
    `Checkpoint '${checkpointId}' was not found.`,
    { agentId, sessionId, checkpointId }
  );

  ensureCondition(
    checkpoint.agentId === agentId && checkpoint.sessionId === sessionId,
    "CHECKPOINT_NOT_FOUND",
    `Checkpoint '${checkpointId}' does not belong to session '${sessionId}'.`,
    { checkpointId, agentId, sessionId }
  );

  return checkpoint;
}

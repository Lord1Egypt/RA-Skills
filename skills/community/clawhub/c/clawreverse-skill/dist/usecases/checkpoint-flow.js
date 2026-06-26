import { manifest } from "../core/contracts.js";
import { shouldCreateCheckpointForTool } from "../core/tooling.js";

function syncRuntimeCursor(services, ctx) {
  return services.runtimeCursorManager.update(
    ctx.agentId,
    ctx.sessionId,
    (state) => {
      state.activeHeadEntryId = ctx.entryId;
      state.currentRunId = ctx.runId ?? state.currentRunId ?? null;
      return state;
    },
    {
      activeHeadEntryId: ctx.entryId,
      currentRunId: ctx.runId ?? null
    }
  );
}

export async function captureCheckpointBeforeTool({ services, logger, ctx }) {
  await syncRuntimeCursor(services, ctx);

  if (!shouldCreateCheckpointForTool(ctx)) {
    logger.info?.(
      `[${manifest.id}] skipped checkpoint for read-only tool agent='${ctx.agentId}' session='${ctx.sessionId}' tool='${ctx.toolName}'`
    );
    return null;
  }

  const checkpoint = await services.checkpointManager.create(ctx);
  logger.info?.(
    `[${manifest.id}] created checkpoint '${checkpoint.checkpointId}' for session '${ctx.sessionId}' before tool '${ctx.toolName}'`
  );
  return checkpoint;
}

export async function reconcileCheckpointAfterTool({ services, ctx }) {
  const runtimeState = await syncRuntimeCursor(services, ctx);

  if (ctx.toolCallId && shouldCreateCheckpointForTool(ctx)) {
    await services.checkpointManager.reconcile(ctx);
  }

  return runtimeState;
}

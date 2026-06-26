function compactObject(value) {
  return Object.fromEntries(
    Object.entries(value).filter(([, entryValue]) => entryValue !== null && entryValue !== undefined)
  );
}

function buildCompanionRuntimeState(runtimeState = {}) {
  return compactObject({
    activeRequests: Array.isArray(runtimeState.activeRequests)
      ? runtimeState.activeRequests
          .map((entry) =>
            compactObject({
              requestId: entry.requestId,
              channelKey: entry.channelKey,
              agentName: entry.agentName,
              stage: entry.stage,
              lastHeartbeatAt: entry.lastHeartbeatAt,
            })
          )
          .filter((entry) => entry.requestId)
      : undefined,
    lastDesiredSyncAt: runtimeState.lastDesiredSyncAt,
    lastInventoryUploadedAt: runtimeState.lastInventoryUploadedAt,
    lastApplyStartedAt: runtimeState.lastApplyStartedAt,
    lastApplyCompletedAt: runtimeState.lastApplyCompletedAt,
    lastReconciledAt: runtimeState.lastReconciledAt,
    lastAppliedDesiredConfigVersion: runtimeState.lastAppliedDesiredConfigVersion,
    lastAppliedManagedFragmentPath: runtimeState.lastAppliedManagedFragmentPath,
    lastAppliedManagedFragmentHash: runtimeState.lastAppliedManagedFragmentHash,
    driftDetected: runtimeState.driftDetected,
    driftReason: runtimeState.driftReason,
  });
}

module.exports = {
  buildCompanionRuntimeState,
};

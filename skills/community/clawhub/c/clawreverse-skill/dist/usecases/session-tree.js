import { ensureCondition } from "../core/errors.js";
import { appendMapValue, compareTimeline } from "../core/persistence.js";

function buildSessionTreeKey(agentId, sessionId) {
  return `${agentId}::${sessionId}`;
}

export async function buildSessionTree({
  services,
  agentId,
  sessionId,
  nodeId,
  checkpointId
}) {
  const requestedAgentId = typeof agentId === "string" ? agentId.trim() : "";
  const requestedSessionId = typeof sessionId === "string" ? sessionId.trim() : "";
  const requestedNodeId = typeof nodeId === "string" && nodeId.trim()
    ? nodeId.trim()
    : typeof checkpointId === "string" && checkpointId.trim()
      ? checkpointId.trim()
      : "";
  const sessionIndexes = await services.registry.listSessionIndexes();
  const sessionIndexByKey = new Map();
  const sessionKeysBySessionId = new Map();
  const checkpointsById = new Map();
  const checkpointsBySessionKey = new Map();

  for (const sessionIndex of sessionIndexes) {
    const sessionKey = buildSessionTreeKey(sessionIndex.agentId, sessionIndex.sessionId);
    sessionIndexByKey.set(sessionKey, sessionIndex);
    appendMapValue(sessionKeysBySessionId, sessionIndex.sessionId, sessionKey);
    checkpointsBySessionKey.set(sessionKey, sessionIndex.checkpoints ?? []);

    for (const checkpoint of sessionIndex.checkpoints ?? []) {
      checkpointsById.set(checkpoint.checkpointId, checkpoint);
    }
  }

  const resolveSessionKey = (resolvedAgentId, resolvedSessionId) => {
    if (!resolvedSessionId) {
      return null;
    }

    if (resolvedAgentId) {
      const directKey = buildSessionTreeKey(resolvedAgentId, resolvedSessionId);
      return sessionIndexByKey.has(directKey) ? directKey : null;
    }

    return (sessionKeysBySessionId.get(resolvedSessionId) ?? [])[0] ?? null;
  };

  const resolveCheckpointByEntry = (resolvedAgentId, resolvedSessionId, entryId) => {
    if (!resolvedSessionId || !entryId) {
      return null;
    }

    const resolvedSessionKey = resolveSessionKey(resolvedAgentId, resolvedSessionId);
    const checkpoints = resolvedSessionKey ? checkpointsBySessionKey.get(resolvedSessionKey) ?? [] : [];
    return checkpoints.find((checkpoint) => checkpoint.entryId === entryId) ?? null;
  };

  const normalizedBranches = (await services.registry.listBranches())
    .map((branch) => {
      const resolvedChildSessionKey = resolveSessionKey(branch.newAgentId, branch.newSessionId);
      const resolvedSourceSessionKey = resolveSessionKey(branch.sourceAgentId, branch.sourceSessionId);
      const sourceCheckpoint = branch.sourceCheckpointId
        ? checkpointsById.get(branch.sourceCheckpointId) ?? null
        : resolveCheckpointByEntry(branch.sourceAgentId, branch.sourceSessionId, branch.sourceEntryId);
      const childRootCheckpoint = resolvedChildSessionKey
        ? (checkpointsBySessionKey.get(resolvedChildSessionKey) ?? [])[0] ?? null
        : null;

      return {
        ...branch,
        reason: branch.reason ?? branch.branchType ?? "branch",
        sourceSessionKey: resolvedSourceSessionKey,
        childSessionKey: resolvedChildSessionKey,
        sourceCheckpointId: sourceCheckpoint?.checkpointId ?? branch.sourceCheckpointId ?? null,
        childRootCheckpointId: childRootCheckpoint?.checkpointId ?? null
      };
    })
    .filter((branch) => branch.childSessionKey || branch.sourceSessionKey || branch.sourceCheckpointId);
  const childSessionKeys = new Set(
    normalizedBranches
      .map((branch) => branch.childSessionKey)
      .filter(Boolean)
  );
  let rootCheckpoint = requestedNodeId ? checkpointsById.get(requestedNodeId) ?? null : null;
  let resolvedBy = requestedNodeId ? "node" : requestedSessionId ? "session" : "default";

  if (requestedNodeId && !rootCheckpoint) {
    rootCheckpoint = await services.checkpointManager.get(requestedNodeId);
  }

  if (!requestedNodeId) {
    let targetSessionIndex = null;

    if (requestedSessionId) {
      const sessionKey = resolveSessionKey(requestedAgentId, requestedSessionId);
      targetSessionIndex = sessionKey ? sessionIndexByKey.get(sessionKey) ?? null : null;
      ensureCondition(
        targetSessionIndex,
        "SESSION_NOT_FOUND",
        requestedAgentId
          ? `Session '${requestedSessionId}' was not found for agent '${requestedAgentId}'.`
          : `Session '${requestedSessionId}' was not found in checkpoint history.`,
        { agentId: requestedAgentId || undefined, sessionId: requestedSessionId }
      );
    } else {
      const candidates = sessionIndexes.filter((entry) => !requestedAgentId || entry.agentId === requestedAgentId);

      ensureCondition(
        candidates.length > 0,
        "SESSION_NOT_FOUND",
        requestedAgentId
          ? `No checkpoint sessions were found for agent '${requestedAgentId}'.`
          : "No checkpoint sessions were found.",
        { agentId: requestedAgentId || undefined }
      );

      const rootCandidates = candidates.filter(
        (entry) => !childSessionKeys.has(buildSessionTreeKey(entry.agentId, entry.sessionId))
      );
      const sortedCandidates = [...(rootCandidates.length > 0 ? rootCandidates : candidates)]
        .sort((left, right) => compareTimeline(left, right, ["agentId", "sessionId"]));
      targetSessionIndex = sortedCandidates[0] ?? null;
    }

    rootCheckpoint = targetSessionIndex?.checkpoints?.[0] ?? null;
  }

  ensureCondition(
    rootCheckpoint,
    "CHECKPOINT_NOT_FOUND",
    requestedNodeId
      ? `Node '${requestedNodeId}' was not found.`
      : requestedSessionId
        ? `Session '${requestedSessionId}' does not have any checkpoints.`
        : requestedAgentId
          ? `Agent '${requestedAgentId}' does not have any checkpoints yet.`
          : "No checkpoints were found.",
    {
      agentId: requestedAgentId || undefined,
      sessionId: requestedSessionId || undefined,
      checkpointId: requestedNodeId || undefined
    }
  );

  const rootSessionKey = buildSessionTreeKey(rootCheckpoint.agentId, rootCheckpoint.sessionId);

  if (!sessionIndexByKey.has(rootSessionKey)) {
    const rootSessionCheckpoints = await services.checkpointManager.list(rootCheckpoint.agentId, rootCheckpoint.sessionId);
    sessionIndexByKey.set(rootSessionKey, {
      agentId: rootCheckpoint.agentId,
      sessionId: rootCheckpoint.sessionId,
      checkpoints: rootSessionCheckpoints
    });
    checkpointsBySessionKey.set(rootSessionKey, rootSessionCheckpoints);

    for (const checkpoint of rootSessionCheckpoints) {
      checkpointsById.set(checkpoint.checkpointId, checkpoint);
    }
  }

  const branchesBySourceCheckpointId = new Map();

  for (const branch of normalizedBranches) {
    if (!branch.sourceCheckpointId || !branch.childRootCheckpointId) {
      continue;
    }

    appendMapValue(branchesBySourceCheckpointId, branch.sourceCheckpointId, branch);
  }

  for (const [sourceCheckpointId, branches] of branchesBySourceCheckpointId.entries()) {
    branches.sort((left, right) => {
      const leftCheckpoint = checkpointsById.get(left.childRootCheckpointId) ?? left;
      const rightCheckpoint = checkpointsById.get(right.childRootCheckpointId) ?? right;
      return compareTimeline(leftCheckpoint, rightCheckpoint, ["branchId", "childRootCheckpointId"]);
    });
    branchesBySourceCheckpointId.set(sourceCheckpointId, branches);
  }

  const buildTree = (currentCheckpointId, incoming = null, lineage = new Set()) => {
    if (lineage.has(currentCheckpointId)) {
      return null;
    }

    const checkpoint = checkpointsById.get(currentCheckpointId) ?? null;

    if (!checkpoint) {
      return null;
    }

    const nextLineage = new Set(lineage);
    nextLineage.add(currentCheckpointId);

    const sessionKey = buildSessionTreeKey(checkpoint.agentId, checkpoint.sessionId);
    const sessionCheckpoints = checkpointsBySessionKey.get(sessionKey) ?? [];
    const position = sessionCheckpoints.findIndex((item) => item.checkpointId === currentCheckpointId);
    const linearChild = position >= 0 ? sessionCheckpoints[position + 1] ?? null : null;
    const branchChildren = branchesBySourceCheckpointId.get(currentCheckpointId) ?? [];
    const children = [];

    if (linearChild) {
      const childTree = buildTree(linearChild.checkpointId, {
        type: "linear",
        reason: "session"
      }, nextLineage);
      if (childTree) {
        children.push(childTree);
      }
    }

    for (const branch of branchChildren) {
      const childTree = buildTree(branch.childRootCheckpointId, {
        type: "branch",
        reason: branch.reason ?? branch.branchType ?? "branch",
        branchId: branch.branchId,
        branchType: branch.branchType ?? null,
        sourceSessionId: branch.sourceSessionId ?? null,
        targetSessionId: branch.newSessionId ?? null,
        targetAgentId: branch.newAgentId ?? null
      }, nextLineage);
      if (childTree) {
        children.push(childTree);
      }
    }

    return {
      checkpointId: checkpoint.checkpointId,
      agentId: checkpoint.agentId,
      sessionId: checkpoint.sessionId,
      entryId: checkpoint.entryId,
      nodeIndex: checkpoint.nodeIndex,
      toolName: checkpoint.toolName,
      summary: checkpoint.summary ?? null,
      status: checkpoint.status ?? null,
      createdAt: checkpoint.createdAt ?? null,
      incomingType: incoming?.type ?? (position > 0 ? "linear" : null),
      incomingReason: incoming?.reason ?? (position > 0 ? "session" : null),
      incomingBranchId: incoming?.branchId ?? null,
      incomingBranchType: incoming?.branchType ?? null,
      children
    };
  };

  const tree = buildTree(rootCheckpoint.checkpointId);
  const seenCheckpoints = new Set();
  const seenSessions = new Set();
  let totalBranches = 0;

  const visit = (node) => {
    if (!node || seenCheckpoints.has(node.checkpointId)) {
      return;
    }

    seenCheckpoints.add(node.checkpointId);
    seenSessions.add(buildSessionTreeKey(node.agentId, node.sessionId));

    if (node.incomingType === "branch") {
      totalBranches += 1;
    }

    for (const child of node.children ?? []) {
      visit(child);
    }
  };

  visit(tree);

  return {
    agentId: rootCheckpoint.agentId,
    sessionId: rootCheckpoint.sessionId,
    root: {
      checkpointId: rootCheckpoint.checkpointId,
      agentId: rootCheckpoint.agentId,
      sessionId: rootCheckpoint.sessionId,
      entryId: rootCheckpoint.entryId,
      nodeIndex: rootCheckpoint.nodeIndex,
      resolvedBy,
      usedDefaultRoot: resolvedBy === "default"
    },
    tree,
    totalNodes: seenCheckpoints.size,
    totalSessions: seenSessions.size,
    totalBranches
  };
}

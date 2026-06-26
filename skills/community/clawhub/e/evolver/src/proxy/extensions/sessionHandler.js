'use strict';

// SessionHandler -- enables agents to proactively create, join, and manage
// collaboration sessions via the Hub. Extends Evolver's proxy with full
// peer-to-peer swarm collaboration capability (session lifecycle + subtask
// delegation), shifting from passive Hub-orchestrated mode to agent-initiated
// mesh collaboration.

class SessionHandler {
  constructor({ store, logger } = {}) {
    this.store = store;
    this.logger = logger || console;
  }

  createSession({ title, description, inviteNodeIds, maxParticipants } = {}) {
    if (!title) throw new Error('title is required');

    return this.store.send({
      type: 'session_create',
      payload: {
        title,
        description: description || '',
        invite_node_ids: Array.isArray(inviteNodeIds) ? inviteNodeIds.slice(0, 10) : [],
        max_participants: Math.max(2, Math.min(20, Number(maxParticipants) || 5)),
        created_at: new Date().toISOString(),
      },
      priority: 'high',
    });
  }

  joinSession({ sessionId } = {}) {
    if (!sessionId) throw new Error('sessionId is required');

    return this.store.send({
      type: 'session_join',
      payload: {
        session_id: sessionId,
        joined_at: new Date().toISOString(),
      },
      priority: 'normal',
    });
  }

  leaveSession({ sessionId } = {}) {
    if (!sessionId) throw new Error('sessionId is required');

    return this.store.send({
      type: 'session_leave',
      payload: {
        session_id: sessionId,
        left_at: new Date().toISOString(),
      },
      priority: 'normal',
    });
  }

  sendMessage({ sessionId, toNodeId, msgType, payload } = {}) {
    if (!sessionId) throw new Error('sessionId is required');

    const safePayload = payload && typeof payload === 'object' ? payload : {};
    const serialized = JSON.stringify(safePayload);
    if (serialized.length > 16000) throw new Error('payload too large (max 16KB)');

    return this.store.send({
      type: 'session_message',
      payload: {
        session_id: sessionId,
        to_node_id: toNodeId || null,
        msg_type: msgType || 'context_update',
        payload: safePayload,
        sent_at: new Date().toISOString(),
      },
      priority: 'normal',
    });
  }

  delegateSubtask({ sessionId, toNodeId, title, description, role } = {}) {
    if (!sessionId) throw new Error('sessionId is required');
    if (!title) throw new Error('title is required');

    const VALID_ROLES = ['builder', 'planner', 'reviewer'];
    const safeRole = VALID_ROLES.includes(role) ? role : 'builder';

    return this.store.send({
      type: 'session_delegate',
      payload: {
        session_id: sessionId,
        to_node_id: toNodeId || null,
        title,
        description: description || '',
        role: safeRole,
        delegated_at: new Date().toISOString(),
      },
      priority: 'high',
    });
  }

  submitResult({ sessionId, taskId, resultAssetId, summary } = {}) {
    if (!sessionId) throw new Error('sessionId is required');
    if (!taskId) throw new Error('taskId is required');

    const safeSummary = typeof summary === 'string' ? summary.slice(0, 200) : '';

    return this.store.send({
      type: 'session_submit',
      payload: {
        session_id: sessionId,
        task_id: taskId,
        result_asset_id: resultAssetId || null,
        summary: safeSummary,
        submitted_at: new Date().toISOString(),
      },
      priority: 'high',
    });
  }

  pollInvites({ limit } = {}) {
    return this.store.poll({
      type: 'collaboration_invite',
      limit: limit || 10,
    });
  }

  pollSessionEvents({ limit } = {}) {
    return this.store.poll({
      type: 'session_event',
      limit: limit || 20,
    });
  }

  listActiveSessions() {
    const sessionMsgs = this.store.list({
      type: 'session_create',
      direction: 'outbound',
      limit: 50,
    });
    return sessionMsgs;
  }
}

module.exports = { SessionHandler };

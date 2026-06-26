'use strict';

const { PROXY_PROTOCOL_VERSION, SCHEMA_VERSION } = require('../mailbox/store');

function buildRoutes(store, proxyHandlers, taskMonitor, extensions) {
  const {
    dmHandler,
    skillUpdater,
    getHubMailboxStatus,
    sessionHandler,
    messagesHandler,
    responsesHandler,
    geminiHandler,
    chatCompletionsHandler,
    modelsHandler,
    ollamaChatHandler,
    ollamaGenerateHandler,
    vertexHandler,
  } = extensions || {};
  const routes = {
    // -- Mailbox --
    'POST /mailbox/send': async ({ body }) => {
      if (!body.type) throw Object.assign(new Error('type is required'), { statusCode: 400 });
      if (!body.payload) throw Object.assign(new Error('payload is required'), { statusCode: 400 });
      const result = store.send({
        type: body.type,
        payload: body.payload,
        channel: body.channel,
        priority: body.priority,
        refId: body.ref_id,
        expiresAt: body.expires_at,
      });
      return { body: result };
    },

    'POST /mailbox/poll': async ({ body }) => {
      const messages = store.poll({
        channel: body.channel,
        type: body.type,
        limit: body.limit,
      });
      return { body: { messages, count: messages.length } };
    },

    'POST /mailbox/ack': async ({ body }) => {
      if (!body.message_ids) throw Object.assign(new Error('message_ids is required'), { statusCode: 400 });
      const count = store.ack(body.message_ids);
      return { body: { acknowledged: count } };
    },

    'GET /mailbox/list': async ({ query }) => {
      if (!query.type) throw Object.assign(new Error('type query param is required'), { statusCode: 400 });
      const messages = store.list({
        type: query.type,
        direction: query.direction,
        status: query.status,
        limit: Number(query.limit) || 20,
        offset: Number(query.offset) || 0,
      });
      return { body: { messages, count: messages.length } };
    },

    'GET /mailbox/status/:id': async ({ params }) => {
      const msg = store.getById(params.id);
      if (!msg) throw Object.assign(new Error('Message not found'), { statusCode: 404 });
      return { body: msg };
    },

    // -- Asset (proxy HTTP) --
    'POST /asset/validate': async ({ body }) => {
      if (!body.asset_id && !body.assets) {
        throw Object.assign(new Error('asset_id or assets is required'), { statusCode: 400 });
      }
      const result = await proxyHandlers.assetValidate(body);
      return { body: result };
    },

    'POST /asset/fetch': async ({ body }) => {
      const result = await proxyHandlers.assetFetch(body);
      return { body: result };
    },

    'POST /asset/search': async ({ body }) => {
      const result = await proxyHandlers.assetSearch(body);
      return { body: result };
    },

    'POST /asset/submit': async ({ body }) => {
      // The publish path builds a bundle from full asset objects; a bare
      // asset_id is not a valid input here (Bugbot #256 Medium — route used to
      // accept asset_id the handler then ignored).
      if (!body.assets && !body.asset) {
        throw Object.assign(new Error('assets (array) or asset (single object) is required'), { statusCode: 400 });
      }
      // Publish synchronously via the signed Gene+Capsule bundle path
      // (POST /a2a/publish). The old `asset_submit` mailbox dispatch is gated
      // off at the Hub (A2A_MAILBOX_ASSET_SUBMIT_ENABLED), so it silently
      // failed; the Hub now enforces bundles. Returns the per-asset Hub result.
      const result = await proxyHandlers.assetPublish(body);
      return { body: result };
    },

    'POST /conversation/distill': async ({ body }) => {
      const { distillConversation } = require('../../gep/conversationDistiller');
      const input = body || {};
      const distill = distillConversation(input, { persist: input.persist !== false });
      if (!distill.ok) return { body: distill };

      let publishResult = null;
      if (input.publish !== false) {
        publishResult = await proxyHandlers.assetPublish({
          assets: [distill.gene, distill.capsule].filter(Boolean),
        });
      }

      return {
        body: {
          ...distill,
          queued: false,
          published: Boolean(publishResult),
          publish_result: publishResult,
        },
      };
    },

    'GET /asset/submissions': async ({ query }) => {
      const submissions = store.list({
        type: 'asset_submit',
        direction: 'outbound',
        status: query.status || undefined,
        limit: Number(query.limit) || 20,
        offset: Number(query.offset) || 0,
      });
      const submissionIds = new Set(submissions.map(s => s.id));
      const resultMap = {};
      for (const [, msg] of store._messages) {
        if (msg.type !== 'asset_submit_result' || msg.direction !== 'inbound') continue;
        const refId = msg.payload?.ref_id;
        if (refId && submissionIds.has(refId)) resultMap[refId] = msg;
      }
      const enriched = submissions.map(s => ({
        ...s,
        result: resultMap[s.id] ? { ...resultMap[s.id] } : null,
      }));
      return { body: { submissions: enriched, count: enriched.length } };
    },

    // -- Task --
    'POST /task/subscribe': async ({ body }) => {
      if (taskMonitor) {
        const result = taskMonitor.subscribe(body.capability_filter || body.filters || []);
        return { body: result };
      }
      const result = store.send({
        type: 'task_subscribe',
        payload: body || {},
      });
      return { body: result };
    },

    'POST /task/unsubscribe': async ({ body }) => {
      if (taskMonitor) {
        const result = taskMonitor.unsubscribe();
        return { body: result };
      }
      const result = store.send({
        type: 'task_unsubscribe',
        payload: body || {},
      });
      return { body: result };
    },

    'GET /task/list': async ({ query }) => {
      const messages = store.poll({
        type: 'task_available',
        limit: Number(query.limit) || 20,
      });
      return { body: { tasks: messages, count: messages.length } };
    },

    'POST /task/claim': async ({ body }) => {
      if (!body.task_id) throw Object.assign(new Error('task_id is required'), { statusCode: 400 });
      const result = store.send({
        type: 'task_claim',
        payload: body,
        priority: 'high',
      });
      if (taskMonitor) taskMonitor.recordClaim(body.task_id);
      return { body: result };
    },

    'POST /task/complete': async ({ body }) => {
      if (!body.task_id) throw Object.assign(new Error('task_id is required'), { statusCode: 400 });
      const result = store.send({
        type: 'task_complete',
        payload: body,
      });
      if (taskMonitor) taskMonitor.recordComplete(body.task_id, body.started_at);
      return { body: result };
    },

    'GET /task/metrics': async () => {
      if (!taskMonitor) {
        return { body: { subscribed: false, metrics: null } };
      }
      return { body: taskMonitor.getMetrics() };
    },

    // -- DM (Direct Message) --
    'POST /dm/send': async ({ body }) => {
      if (!body.recipient_node_id) {
        throw Object.assign(new Error('recipient_node_id is required'), { statusCode: 400 });
      }
      if (!body.content) {
        throw Object.assign(new Error('content is required'), { statusCode: 400 });
      }
      if (dmHandler) {
        const result = dmHandler.send({
          recipientNodeId: body.recipient_node_id,
          content: body.content,
          metadata: body.metadata,
        });
        return { body: result };
      }
      const result = store.send({
        type: 'dm',
        payload: {
          recipient_node_id: body.recipient_node_id,
          content: body.content,
          metadata: body.metadata || {},
        },
      });
      return { body: result };
    },

    'POST /dm/poll': async ({ body }) => {
      if (dmHandler) {
        const messages = dmHandler.poll({ limit: body.limit });
        return { body: { messages, count: messages.length } };
      }
      const messages = store.poll({ type: 'dm', limit: body.limit || 20 });
      return { body: { messages, count: messages.length } };
    },

    'GET /dm/list': async ({ query }) => {
      if (dmHandler) {
        const messages = dmHandler.list({
          limit: Number(query.limit) || 20,
          offset: Number(query.offset) || 0,
        });
        return { body: { messages, count: messages.length } };
      }
      const messages = store.list({
        type: 'dm',
        limit: Number(query.limit) || 20,
        offset: Number(query.offset) || 0,
      });
      return { body: { messages, count: messages.length } };
    },

    // -- Session (Collaboration) --
    'POST /session/create': async ({ body }) => {
      if (!body.title) throw Object.assign(new Error('title is required'), { statusCode: 400 });
      if (sessionHandler) {
        const result = sessionHandler.createSession({
          title: body.title,
          description: body.description,
          inviteNodeIds: body.invite_node_ids,
          maxParticipants: body.max_participants,
        });
        return { body: result };
      }
      const result = store.send({
        type: 'session_create',
        payload: {
          title: body.title,
          description: body.description || '',
          invite_node_ids: body.invite_node_ids || [],
          max_participants: body.max_participants || 5,
        },
      });
      return { body: result };
    },

    'POST /session/join': async ({ body }) => {
      if (!body.session_id) throw Object.assign(new Error('session_id is required'), { statusCode: 400 });
      if (sessionHandler) {
        const result = sessionHandler.joinSession({ sessionId: body.session_id });
        return { body: result };
      }
      const result = store.send({ type: 'session_join', payload: { session_id: body.session_id } });
      return { body: result };
    },

    'POST /session/leave': async ({ body }) => {
      if (!body.session_id) throw Object.assign(new Error('session_id is required'), { statusCode: 400 });
      if (sessionHandler) {
        const result = sessionHandler.leaveSession({ sessionId: body.session_id });
        return { body: result };
      }
      const result = store.send({ type: 'session_leave', payload: { session_id: body.session_id } });
      return { body: result };
    },

    'POST /session/message': async ({ body }) => {
      if (!body.session_id) throw Object.assign(new Error('session_id is required'), { statusCode: 400 });
      if (sessionHandler) {
        const result = sessionHandler.sendMessage({
          sessionId: body.session_id,
          toNodeId: body.to_node_id,
          msgType: body.msg_type,
          payload: body.payload,
        });
        return { body: result };
      }
      const result = store.send({
        type: 'session_message',
        payload: {
          session_id: body.session_id,
          to_node_id: body.to_node_id || null,
          msg_type: body.msg_type || 'context_update',
          payload: body.payload || {},
        },
      });
      return { body: result };
    },

    'POST /session/delegate': async ({ body }) => {
      if (!body.session_id) throw Object.assign(new Error('session_id is required'), { statusCode: 400 });
      if (!body.title) throw Object.assign(new Error('title is required'), { statusCode: 400 });
      if (sessionHandler) {
        const result = sessionHandler.delegateSubtask({
          sessionId: body.session_id,
          toNodeId: body.to_node_id,
          title: body.title,
          description: body.description,
          role: body.role,
        });
        return { body: result };
      }
      const result = store.send({
        type: 'session_delegate',
        payload: {
          session_id: body.session_id,
          to_node_id: body.to_node_id || null,
          title: body.title,
          description: body.description || '',
          role: body.role || 'builder',
        },
        priority: 'high',
      });
      return { body: result };
    },

    'POST /session/submit': async ({ body }) => {
      if (!body.session_id) throw Object.assign(new Error('session_id is required'), { statusCode: 400 });
      if (!body.task_id) throw Object.assign(new Error('task_id is required'), { statusCode: 400 });
      if (sessionHandler) {
        const result = sessionHandler.submitResult({
          sessionId: body.session_id,
          taskId: body.task_id,
          resultAssetId: body.result_asset_id,
          summary: body.summary,
        });
        return { body: result };
      }
      const result = store.send({
        type: 'session_submit',
        payload: {
          session_id: body.session_id,
          task_id: body.task_id,
          result_asset_id: body.result_asset_id || null,
          summary: body.summary || '',
        },
        priority: 'high',
      });
      return { body: result };
    },

    'POST /session/invites/poll': async ({ body }) => {
      if (sessionHandler) {
        const messages = sessionHandler.pollInvites({ limit: body.limit });
        return { body: { messages, count: messages.length } };
      }
      const messages = store.poll({ type: 'collaboration_invite', limit: body.limit || 10 });
      return { body: { messages, count: messages.length } };
    },

    'GET /session/list': async ({ query }) => {
      if (sessionHandler) {
        const sessions = sessionHandler.listActiveSessions();
        return { body: { sessions, count: sessions.length } };
      }
      const sessions = store.list({ type: 'session_create', direction: 'outbound', limit: Number(query.limit) || 20 });
      return { body: { sessions, count: sessions.length } };
    },

    // -- System --
    'GET /proxy/status': async () => {
      const outPending = store.countPending({ direction: 'outbound' });
      const inPending = store.countPending({ direction: 'inbound' });
      const nodeId = store.getState('node_id');
      const lastSync = store.getState('last_sync_at');
      const lastSyncError = store.getState('last_sync_error');
      const hubAuthStatus = store.getState('hub_auth_status');
      const reauthBackoffUntil = store.getState('reauth_backoff_until');
      const helloRateLimitUntil = store.getState('hello_rate_limit_until');
      return {
        body: {
          status: 'running',
          node_id: nodeId,
          proxy_protocol_version: PROXY_PROTOCOL_VERSION,
          schema_version: SCHEMA_VERSION,
          outbound_pending: outPending,
          inbound_pending: inPending,
          last_sync_at: lastSync,
          last_sync_error: lastSyncError || null,
          hub_auth_status: hubAuthStatus || null,
          reauth_backoff_until: reauthBackoffUntil || null,
          hello_rate_limit_until: helloRateLimitUntil || null,
        },
      };
    },

    'GET /proxy/config': async () => {
      return {
        body: {
          channel: 'evomap-hub',
          proxy_protocol_version: PROXY_PROTOCOL_VERSION,
          schema_version: SCHEMA_VERSION,
        },
      };
    },

    'GET /proxy/hub-status': async () => {
      if (!getHubMailboxStatus) return { body: { error: 'not_available' } };
      const hubStatus = await getHubMailboxStatus();
      return { body: hubStatus };
    },

    // -- ATP (Agent Transaction Protocol) passthrough --
    // #460 Bug 2: src/atp/hubClient.js historically bypassed the proxy and
    // called the hub directly. When EVOMAP_PROXY=1, hubClient now routes its
    // traffic here so the proxy is the single egress point (audit + offline
    // behavior match the rest of the A2A surface).
    //
    // Security: sender_id and node_id are FORCED to the proxy's own node_id.
    // Callers cannot impersonate another node through the proxy, even if they
    // pass a different sender_id in the body or query string.
    'POST /atp/order': async ({ body }) => {
      const override = { ...(body || {}), sender_id: store.getState('node_id') };
      const result = await proxyHandlers.atpPost('/a2a/atp/order', override);
      return { body: result };
    },

    'POST /atp/deliver': async ({ body }) => {
      const override = { ...(body || {}), sender_id: store.getState('node_id') };
      const result = await proxyHandlers.atpPost('/a2a/atp/deliver', override);
      return { body: result };
    },

    'POST /atp/verify': async ({ body }) => {
      const override = { ...(body || {}), sender_id: store.getState('node_id') };
      const result = await proxyHandlers.atpPost('/a2a/atp/verify', override);
      return { body: result };
    },

    'POST /atp/settle': async ({ body }) => {
      const override = { ...(body || {}), sender_id: store.getState('node_id') };
      const result = await proxyHandlers.atpPost('/a2a/atp/settle', override);
      return { body: result };
    },

    'POST /atp/dispute': async ({ body }) => {
      const override = { ...(body || {}), sender_id: store.getState('node_id') };
      const result = await proxyHandlers.atpPost('/a2a/atp/dispute', override);
      return { body: result };
    },

    'GET /atp/merchant/tier': async ({ query }) => {
      const nodeId = store.getState('node_id');
      const result = await proxyHandlers.atpGet('/a2a/atp/merchant/tier', {
        node_id: query.node_id || nodeId,
      });
      return { body: result };
    },

    'GET /atp/order/:orderId': async ({ params }) => {
      const result = await proxyHandlers.atpGet('/a2a/atp/order/' + encodeURIComponent(params.orderId));
      return { body: result };
    },

    'GET /atp/proofs': async ({ query }) => {
      const nodeId = store.getState('node_id');
      const q = { node_id: nodeId };
      if (query.role) q.role = query.role;
      if (query.status) q.status = query.status;
      if (query.limit) q.limit = query.limit;
      const result = await proxyHandlers.atpGet('/a2a/atp/proofs', q);
      return { body: result };
    },

    'GET /atp/policy': async () => {
      const result = await proxyHandlers.atpGet('/a2a/atp/policy');
      return { body: result };
    },
  };

  // Phase C: only register /v1/messages when the proxy was built with a
  // messages handler (i.e. _proxyAnthropic is available). Slice 5 wires it
  // unconditionally so the route exists on every proxy startup; slice 6 adds
  // EVOMAP_ROUTER_ENABLED behavior inside the handler.
  if (messagesHandler) {
    routes['POST /v1/messages'] = messagesHandler;
  }
  if (responsesHandler) {
    routes['POST /v1/responses'] = responsesHandler;
  }
  if (geminiHandler) {
    // Native Gemini path: model + action (generateContent | streamGenerateContent) are one path segment
    // (`<model>:<action>`), matched as :modelAction and split by the handler.
    routes['POST /v1beta/models/:modelAction'] = geminiHandler;
  }
  if (chatCompletionsHandler) {
    // OpenAI Chat Completions ingress (cursor's OpenAI mode + generic OpenAI clients) → OpenAI upstream.
    routes['POST /v1/chat/completions'] = chatCompletionsHandler;
  }
  if (modelsHandler) {
    // Model-list probe (codex/opencode/cursor/SDKs hit it on startup) → routed by anthropic-version header to
    // the Anthropic or OpenAI upstream's /v1/models, so the probe never 404s.
    routes['GET /v1/models'] = modelsHandler;
  }
  if (ollamaChatHandler) {
    // Ollama native ingress (local/self-hosted models) → Ollama upstream, NDJSON streaming.
    routes['POST /api/chat'] = ollamaChatHandler;
  }
  if (ollamaGenerateHandler) {
    routes['POST /api/generate'] = ollamaGenerateHandler;
  }
  if (vertexHandler) {
    // Vertex AI Gemini native path: project/location/model:action across fixed segments + :modelAction.
    routes['POST /v1/projects/:project/locations/:location/publishers/google/models/:modelAction'] = vertexHandler;
  }

  return routes;
}

module.exports = { buildRoutes };

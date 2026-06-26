import express from 'express';
import crypto from 'crypto';
import path from 'path';
import fs from 'fs';

import { auth, API_KEY } from './lib/auth.js';
import { SERVERS, getServerHealth } from './lib/load-balancer.js';
import {
  submitPrompt,
  getHistoryForPrompt,
  getAggregatedHistory,
  getAggregatedQueue,
  proxyView,
  proxyFirstServer,
  proxyGetPath,
} from './lib/comfy-proxy.js';
import {
  MEDIA_DIR,
  oneTimeTokens,
  newToken,
  ensureMediaDirs,
  waitForPrompt,
  findOutputInHistory,
  downloadAndSave,
  listMedia,
  contentTypeForFile,
  gatewayQueue,
  trackPrompt,
  updatePromptStatus,
  getQueueStats,
  startQueueMonitor,
} from './lib/media-manager.js';
import {
  initRegistry,
  listWorkflowsMeta,
  getWorkflow,
  createWorkflow,
  updateWorkflow,
  deleteWorkflow,
  loadWorkflowJson,
  saveWorkflowJsonFile,
  previewSchema,
  applyParamsToWorkflow,
  getLustifyGenerateInfo,
  NAME_TO_ASPECT,
  WORKFLOW_DIR,
} from './lib/workflow-registry.js';
import { mcpRouter } from './lib/mcp-handler.js';
import { promptMap } from './lib/comfy-proxy.js';

const PORT = process.env.PORT || 8188;

ensureMediaDirs();
initRegistry();

// Start background queue monitor (30s interval)
startQueueMonitor(SERVERS, () => promptMap);

const app = express();
app.use(express.json({ limit: '100mb' }));

// ─── ComfyUI proxy endpoints ─────────────────────────────────────

app.post('/prompt', auth, async (req, res) => {
  const result = await submitPrompt(SERVERS, req.body);
  return res.status(result.status).json(result.data);
});

app.get('/history/:prompt_id', auth, async (req, res) => {
  const result = await getHistoryForPrompt(req.params.prompt_id);
  return res.status(result.status).json(result.data);
});

app.get('/history', auth, async (req, res) => {
  const maxResults = parseInt(req.query.max_items, 10) || 200;
  return res.json(await getAggregatedHistory(maxResults));
});

app.get('/queue', auth, async (req, res) => {
  return res.json(await getAggregatedQueue());
});

app.get('/view', auth, async (req, res) => {
  const result = await proxyView(req.query);
  if (!result.ok) {
    return res.status(404).json({ error: 'File not found on any server' });
  }
  res.set('Content-Type', result.contentType);
  return res.send(result.buffer);
});

app.post('/upload/image', auth, async (req, res) => {
  const result = await proxyFirstServer('/upload/image', {
    method: 'POST',
    headers: { ...req.headers, host: undefined, 'content-length': undefined },
    body: JSON.stringify(req.body),
  });
  return res.status(result.status).json(result.data);
});

app.post('/upload/mask', auth, async (req, res) => {
  const result = await proxyFirstServer('/upload/mask', {
    method: 'POST',
    headers: { ...req.headers, host: undefined, 'content-length': undefined },
    body: JSON.stringify(req.body),
  });
  return res.status(result.status).json(result.data);
});

app.get('/system_stats', auth, async (req, res) => {
  const { status, data } = await proxyGetPath('/system_stats', req.query);
  return res.status(status).json(data);
});

app.get(['/object_info', '/extensions', '/embeddings', '/settings'], auth, async (req, res) => {
  const { status, data } = await proxyGetPath(req.path, req.query);
  return res.status(status).json(data);
});

app.get('/object_info/:node_class', auth, async (req, res) => {
  const { status, data } = await proxyGetPath(`/object_info/${req.params.node_class}`, req.query);
  return res.status(status).json(data);
});

app.get('/', auth, async (req, res) => {
  const servers = await getServerHealth();
  const anyOnline = Object.values(servers).some((s) => s.status === 'online');
  return res.json({
    status: anyOnline ? 'ok' : 'degraded',
    gate_version: '2.0',
    servers,
  });
});

app.get('/health', auth, async (req, res) => {
  const servers = await getServerHealth();
  const stats = getQueueStats();
  const payload = {
    servers,
    gateway_queue: stats,
  };
  if (req.query.prompt_id) {
    const { getGenerationStatus } = await import('./lib/media-manager.js');
    payload.generation = getGenerationStatus(req.query.prompt_id);
  }
  return res.json(payload);
});

// ─── Workflow registry CRUD ──────────────────────────────────────

app.get('/workflows', (req, res) => {
  const list = listWorkflowsMeta();
  // Backward compat: also expose { workflows: { id: { type, ext, description } } }
  const workflows = {};
  for (const [id, m] of Object.entries(list)) {
    workflows[id] = {
      type: m.type,
      ext: m.ext,
      description: m.description,
      title: m.title,
    };
  }
  res.json({ workflows: list, registry: workflows });
});

app.get('/workflows/:id', (req, res) => {
  const w = getWorkflow(req.params.id);
  if (!w) return res.status(404).json({ error: 'Workflow not found' });
  return res.json(w);
});

app.post('/workflows', auth, async (req, res) => {
  try {
    const created = createWorkflow(req.body);
    return res.status(201).json(created);
  } catch (e) {
    return res.status(400).json({ error: e.message });
  }
});

app.put('/workflows/:id', auth, async (req, res) => {
  const updated = updateWorkflow(req.params.id, req.body);
  if (!updated) return res.status(404).json({ error: 'Workflow not found' });
  return res.json(updated);
});

app.delete('/workflows/:id', auth, async (req, res) => {
  const removed = deleteWorkflow(req.params.id);
  if (!removed) return res.status(404).json({ error: 'Workflow not found' });
  return res.json({ ok: true, deleted: removed.id });
});

app.get('/workflows/:id/json', auth, (req, res) => {
  const wf = loadWorkflowJson(req.params.id);
  if (!wf) return res.status(404).json({ error: 'Workflow or JSON file not found' });
  return res.json(wf);
});

app.post('/workflows/:id/json', auth, (req, res) => {
  try {
    saveWorkflowJsonFile(req.params.id, req.body);
    return res.json({ ok: true });
  } catch (e) {
    return res.status(e.message.includes('Unknown') ? 404 : 400).json({ error: e.message });
  }
});

app.get('/workflows/:id/preview', (req, res) => {
  const schema = previewSchema(req.params.id);
  if (!schema) return res.status(404).json({ error: 'Workflow not found' });
  return res.json(schema);
});

// ─── Generation ──────────────────────────────────────────────────

async function runGeneration(workflowId, params, options = {}) {
  const meta = getWorkflow(workflowId);
  if (!meta) {
    return { status: 400, data: { error: 'Unknown workflow', available: Object.keys(listWorkflowsMeta()) } };
  }

  let wf;
  try {
    wf = loadWorkflowJson(workflowId);
    if (!wf) throw new Error(`Workflow file not found: ${meta.file}`);
    applyParamsToWorkflow(wf, meta, params);
  } catch (e) {
    return { status: 400, data: { error: e.message } };
  }

  const body = {
    prompt: wf,
    client_id: options.client_id || crypto.randomUUID(),
  };

  const result = await submitPrompt(SERVERS, body);
  if (result.status !== 200) return result;

  const extra = {
    workflow: workflowId,
    params,
  };

  return {
    status: 200,
    data: {
      ...result.data,
      workflow: workflowId,
      server: result.data.server,
      aspect_ratio: params.aspect_ratio,
    },
    meta,
    serverUrl: SERVERS.find((s) => s.id === result.data.server)?.url,
    upstreamPromptId: result.data.upstream_prompt_id,
  };
}

// POST /generate — registry-based generation
app.post('/generate', auth, async (req, res) => {
  const workflowId = req.body.workflow || 'acestep-aio';
  const params = req.body.params ? { ...req.body.params } : { ...req.body };
  delete params.workflow;
  delete params.mode;
  delete params.client_id;
  if (req.body.seed !== undefined) params.seed = req.body.seed;

  const mode = req.body.mode || 'auto';
  const gen = await runGeneration(workflowId, params, { client_id: req.body.client_id });
  if (gen.status !== 200) return res.status(gen.status).json(gen.data);

  const meta = gen.meta;
  const promptId = gen.data.prompt_id;
  const serverId = gen.data.server;
  const upstreamPromptId = gen.data.upstream_prompt_id;

  // Track in gateway queue
  trackPrompt(upstreamPromptId, {
    prompt_type: meta?.type || 'image',
    server_id: serverId,
    server_prompt_id: upstreamPromptId,
    gateway_prompt_id: promptId,
    workflow: workflowId,
    output_node_ids: meta?.output_node_ids || [],
    params,
  });

  if (mode !== 'wait') {
    return res.json({
      ...gen.data,
      mode: 'auto',
      check_url: `/health?prompt_id=${promptId}`,
      file_url: null,
    });
  }

  const server = SERVERS.find((s) => s.id === gen.data.server);
  if (!server) return res.status(502).json({ error: 'Server not found' });

  const waitResult = await waitForPrompt(server.url, upstreamPromptId, 600000);
  if (!waitResult.done || waitResult.status !== 'completed') {
    updatePromptStatus(upstreamPromptId, waitResult.status || 'failed', { terminal_since: Date.now() });
    return res.status(waitResult.status === 'timeout' ? 504 : 500).json({
      error: waitResult.error || waitResult.status,
      prompt_id: promptId,
    });
  }

  await new Promise((r) => setTimeout(r, 3000));
  const output = findOutputInHistory(waitResult.data?.outputs, meta.output_node_ids);
  if (!output) {
    updatePromptStatus(upstreamPromptId, 'failed', { terminal_since: Date.now() });
    return res.status(500).json({ error: 'No output found after completion' });
  }

  try {
    const saved = await downloadAndSave({
      serverUrl: server.url,
      output,
      workflowId,
      workflowType: meta.type,
      ext: meta.ext,
      meta: { params },
    });
    updatePromptStatus(upstreamPromptId, 'completed', {
      file_url: saved.url,
      file_path: saved.file,
      terminal_since: Date.now(),
    });
    return res.json({
      ...gen.data,
      status: 'ok',
      file_url: saved.url,
      filename: saved.filename,
      file_size: saved.file_size,
    });
  } catch (e) {
    updatePromptStatus(upstreamPromptId, 'failed', { terminal_since: Date.now() });
    return res.status(502).json({ error: e.message });
  }
});

app.post('/generate/raw', auth, async (req, res) => {
  const { workflow, mode = 'auto', output_filename, client_id } = req.body;
  if (!workflow || typeof workflow !== 'object') {
    return res.status(400).json({ error: 'workflow object is required' });
  }

  const result = await submitPrompt(SERVERS, {
    prompt: workflow,
    client_id: client_id || crypto.randomUUID(),
  });
  if (result.status !== 200) return res.status(result.status).json(result.data);

  const rawUpstreamPid = result.data.upstream_prompt_id;
  const rawServerId = result.data.server;
  const rawServer = SERVERS.find((s) => s.id === rawServerId);

  // Track raw prompt
  trackPrompt(rawUpstreamPid, {
    prompt_type: 'image',
    server_id: rawServerId,
    server_prompt_id: rawUpstreamPid,
    gateway_prompt_id: result.data.prompt_id,
    workflow: output_filename || 'raw',
    params: {},
  });

  if (mode !== 'wait') {
    return res.json({
      ...result.data,
      mode: 'auto',
      check_url: null,
      file_url: null,
    });
  }

  const waitResult = await waitForPrompt(rawServer.url, rawUpstreamPid, 600000);
  if (!waitResult.done || waitResult.status !== 'completed') {
    updatePromptStatus(rawUpstreamPid, waitResult.status || 'failed', { terminal_since: Date.now() });
    return res.status(waitResult.status === 'timeout' ? 504 : 500).json({
      error: waitResult.error || waitResult.status,
    });
  }

  await new Promise((r) => setTimeout(r, 3000));
  const output = findOutputInHistory(waitResult.data?.outputs);
  if (!output) {
    updatePromptStatus(rawUpstreamPid, 'failed', { terminal_since: Date.now() });
    return res.status(500).json({ error: 'No output found' });
  }

  const ext = (output.filename || '').split('.').pop() || 'bin';
  const wfType = output.mediaKind === 'audio' ? 'audio' : 'image';
  try {
    const saved = await downloadAndSave({
      serverUrl: rawServer.url,
      output,
      workflowId: output_filename || 'raw',
      workflowType: wfType,
      ext,
    });
    updatePromptStatus(rawUpstreamPid, 'completed', {
      file_url: saved.url,
      file_path: saved.file,
      terminal_since: Date.now(),
    });
    return res.json({
      status: 'ok',
      ...result.data,
      file_url: saved.url,
      filename: saved.filename,
      file_size: saved.file_size,
    });
  } catch (e) {
    updatePromptStatus(rawUpstreamPid, 'failed', { terminal_since: Date.now() });
    return res.status(502).json({ error: e.message });
  }
});

app.post('/generate-and-wait', auth, async (req, res) => {
  const workflowName = req.body.workflow || 'acestep-aio';
  const meta = getWorkflow(workflowName);
  if (!meta) {
    return res.status(400).json({
      error: 'Unknown workflow',
      available: Object.keys(listWorkflowsMeta()),
    });
  }

  const params = { ...req.body };
  if (!params.prompt && !params.tags) {
    return res.status(400).json({ error: 'prompt is required' });
  }
  if (!params.prompt && params.tags) params.prompt = params.tags;

  let wf;
  try {
    wf = loadWorkflowJson(workflowName);
    applyParamsToWorkflow(wf, meta, params);
  } catch (e) {
    return res.status(400).json({ error: e.message });
  }

  const submit = await submitPrompt(SERVERS, {
    prompt: wf,
    client_id: req.body.client_id || crypto.randomUUID(),
  });
  if (submit.status !== 200) return res.status(submit.status).json(submit.data);

  const server = SERVERS.find((s) => s.id === submit.data.server);
  const serverPromptId = submit.data.upstream_prompt_id;

  const result = await waitForPrompt(server.url, serverPromptId, 600000);
  if (!result.done) {
    return res.status(504).json({ error: result.error || 'Timeout', server: server.id });
  }
  if (result.status === 'failed' || result.status === 'cancelled') {
    return res.status(500).json({ error: result.error || result.status, server: server.id });
  }

  await new Promise((r) => setTimeout(r, 3000));
  const output = findOutputInHistory(result.data?.outputs, meta.output_node_ids);
  if (!output) {
    return res.status(500).json({
      error: 'Generation completed but no output file found',
      server: server.id,
      prompt_id: serverPromptId,
    });
  }

  try {
    const saved = await downloadAndSave({
      serverUrl: server.url,
      output,
      workflowId: workflowName,
      workflowType: meta.type,
      ext: meta.ext,
      meta: {
        prompt: params.prompt,
        lyrics: params.lyrics || '',
        seed: params.seed || 0,
        aspect_ratio: params.aspect_ratio || '',
        duration: params.duration || 0,
        bpm: params.bpm || 0,
        server: server.id,
        server_prompt_id: serverPromptId,
        model: meta.description,
      },
    });
    return res.json({
      status: 'ok',
      server: server.id,
      workflow: workflowName,
      ...saved,
    });
  } catch (e) {
    return res.status(502).json({ error: `Download/save failed: ${e.message}` });
  }
});



// ─── Media ───────────────────────────────────────────────────────

app.use(
  '/media',
  auth,
  express.static(MEDIA_DIR, {
    setHeaders(res, filePath) {
      res.set('Content-Type', contentTypeForFile(filePath));
    },
  }),
);

app.get('/media-list', (req, res) => {
  res.json(
    listMedia({
      type: req.query.type,
      q: req.query.q || req.query.search,
      limit: req.query.limit,
    }),
  );
});

app.post('/media-link-once', auth, async (req, res) => {
  const { subpath } = req.body || {};
  if (!subpath || typeof subpath !== 'string') {
    return res.status(400).json({ error: 'subpath is required' });
  }
  if (subpath.includes('..')) return res.status(400).json({ error: 'invalid subpath' });

  const allowedRoots = new Set(['images', 'audio', 'video']);
  const parts = subpath.split('/').filter(Boolean);
  if (parts.length < 2) return res.status(400).json({ error: 'subpath must be <root>/<file>' });
  const root = parts[0];
  if (!allowedRoots.has(root)) return res.status(400).json({ error: 'root not allowed' });

  const file = parts.slice(1).join('/');
  const fullPath = path.join(MEDIA_DIR, root, file);
  if (!fs.existsSync(fullPath)) return res.status(404).json({ error: 'file not found' });

  const token = newToken();
  const tokenDuration = req.body?.ttl !== undefined ? parseInt(req.body.ttl) || 15*60*1000 : 365 * 24 * 60 * 60 * 1000;
  const expiresAt = Date.now() + tokenDuration;
  oneTimeTokens.set(token, { subpath, expiresAt });

  const host = process.env.GATEWAY_PUBLIC_HOST || req.get('host');
  const url = `${req.protocol}://${host}/media-once/${token}`;
  return res.json({ ok: true, token, url });
});

app.get('/media-once/:token', async (req, res) => {
  const entry = oneTimeTokens.get(req.params.token);
  if (!entry) return res.status(404).json({ error: 'token invalid or used' });
  if (Date.now() > entry.expiresAt) {
    oneTimeTokens.delete(req.params.token);
    return res.status(410).json({ error: 'token expired' });
  }

  const parts = entry.subpath.split('/').filter(Boolean);
  const root = parts[0];
  const file = parts.slice(1).join('/');
  const fullPath = path.join(MEDIA_DIR, root, file);
  if (!fs.existsSync(fullPath)) return res.status(404).end();

  res.set('Content-Type', contentTypeForFile(fullPath));
  return fs.createReadStream(fullPath).pipe(res);
});

// ─── DRY RUN — export workflow JSON without sending to servers ──

app.post('/generate/dry-run', auth, (req, res) => {
  const workflowId = req.body.workflow || 'acestep-aio';
  const params = req.body.params ? { ...req.body.params } : { ...req.body };
  delete params.workflow;
  delete params.mode;
  delete params.dry_run;

  const meta = getWorkflow(workflowId);
  if (!meta) {
    return res.status(400).json({ error: 'Unknown workflow', available: Object.keys(listWorkflowsMeta()) });
  }

  let wf;
  try {
    wf = loadWorkflowJson(workflowId);
    if (!wf) throw new Error('Workflow file not found');
    applyParamsToWorkflow(wf, meta, params);
  } catch (e) {
    return res.status(400).json({ error: e.message });
  }

  const dryRunOutput = {
    dry_run: true,
    generated_at: new Date().toISOString(),
    workflow: workflowId,
    meta: {
      title: meta.title,
      type: meta.type,
      ext: meta.ext,
      output_node_ids: meta.output_node_ids,
      description: meta.description,
    },
    params_applied: params,
    prompt: wf,
  };

  return res.json(dryRunOutput);
});

// ─── MCP (Model Context Protocol) Endpoint ─────────────────────
// POST /mcp — streamable-http transport for LLM tool discovery

app.post('/mcp', auth, (req, res) => mcpRouter(req, res));

// ─── Start ───────────────────────────────────────────────────────

process.on('unhandledRejection', (e) => console.error('[unhandledRejection]', e));

app.listen(PORT, () => {
  console.log('');
  console.log('╔══════════════════════════════════════════╗');
  console.log('║       Genor-Comfy-Gate v2.0             ║');
  console.log('╠══════════════════════════════════════════╣');
  console.log(`║  Listening on port ${PORT}`);
  console.log('║  (workflows, servers — see /health)');
  console.log('╚══════════════════════════════════════════╝');
  console.log('');
});

import crypto from 'crypto';
import fs from 'fs';
import path from 'path';

export const MEDIA_DIR =
  process.env.MEDIA_DIR || path.join(process.env.HOME || '/data', '.openclaw', 'workspace', 'media', 'comfy');

/**
 * Gateway queue tracking.
 * Map<prompt_id, { status, submitted_at, file_url, file_path, prompt_type, server_id, workflow, timeout_ms }>
 * Statuses: 'submitted', 'running', 'completed', 'failed', 'timeout'
 */
export const gatewayQueue = new Map();

// Timeouts per type
const TIMEOUT_ACE = 15 * 60 * 1000;   // 15 min
const TIMEOUT_IMAGE = 5 * 60 * 1000;  // 5 min
const CLEANUP_AFTER = 60 * 60 * 1000; // 1 hour

export function trackPrompt(promptId, info = {}) {
  const timeoutMs = info.prompt_type === 'audio' ? TIMEOUT_ACE : TIMEOUT_IMAGE;
  gatewayQueue.set(promptId, {
    status: 'submitted',
    submitted_at: Date.now(),
    file_url: null,
    file_path: null,
    prompt_type: info.prompt_type || 'image',
    server_id: info.server_id || null,
    workflow: info.workflow || null,
    timeout_ms: timeoutMs,
    ...info,
  });
}

export function updatePromptStatus(promptId, status, extra = {}) {
  const entry = gatewayQueue.get(promptId);
  if (!entry) return;
  Object.assign(entry, { status, ...extra });
  gatewayQueue.set(promptId, entry);
}

export function getQueueStats() {
  const byStatus = {};
  let total = 0;
  for (const [, entry] of gatewayQueue) {
    total++;
    byStatus[entry.status] = (byStatus[entry.status] || 0) + 1;
  }
  return { total, by_status: byStatus };
}

/**
 * Look up generation status by upstream or gateway prompt_id.
 * @param {string} promptId
 */
export function getGenerationStatus(promptId) {
  let entry = gatewayQueue.get(promptId);
  if (entry) {
    return formatGenerationStatus(promptId, entry);
  }

  // Allow gateway proxy prompt_id — match by server_prompt_id or stored alias
  for (const [upstreamId, e] of gatewayQueue) {
    if (e.gateway_prompt_id === promptId || e.server_prompt_id === promptId) {
      return formatGenerationStatus(upstreamId, e);
    }
  }

  return null;
}

function formatGenerationStatus(promptId, entry) {
  const elapsedMs = Date.now() - (entry.submitted_at || Date.now());
  return {
    prompt_id: promptId,
    upstream_prompt_id: entry.server_prompt_id || promptId,
    gateway_prompt_id: entry.gateway_prompt_id || null,
    status: entry.status,
    server: entry.server_id,
    workflow: entry.workflow,
    file_url: entry.file_url || null,
    file_path: entry.file_path || null,
    error: entry.error || null,
    submitted_at: entry.submitted_at,
    elapsed_ms: elapsedMs,
    timeout_ms: entry.timeout_ms,
  };
}

/**
 * Start background monitor that polls ComfyUI /history for tracked prompts.
 * Auto-downloads completed generations, applies timeouts, cleans up stale entries.
 */
export function startQueueMonitor(SERVERS, getPromptMap) {
  setInterval(async () => {
    for (const [promptId, entry] of gatewayQueue) {
      // Skip already-terminal entries
      if (['completed', 'failed', 'timeout'].includes(entry.status)) {
        // Cleanup stale entries after 1 hour
        if (entry.terminal_since && Date.now() - entry.terminal_since > CLEANUP_AFTER) {
          gatewayQueue.delete(promptId);
        }
        continue;
      }

      // Check timeout
      if (Date.now() - entry.submitted_at > entry.timeout_ms) {
        updatePromptStatus(promptId, 'timeout', { terminal_since: Date.now() });
        // suppressed: [queue-monitor] TIMEOUT
        continue;
      }

      // Need the server URL to poll history
      const server = SERVERS.find((s) => s.id === entry.server_id);
      if (!server) {
        // Try to resolve via promptMap if available
        const pMap = typeof getPromptMap === 'function' ? getPromptMap() : null;
        const mapped = pMap?.get(promptId);
        if (mapped?.server) {
          entry.server_id = mapped.server.id;
          continue; // re-eval next cycle
        }
        continue;
      }

      // Determine the upstream prompt_id to poll
      // If we stored it directly
      let upstreamId = entry.server_prompt_id || promptId;

      try {
        const hResp = await fetch(`${server.url}/history/${upstreamId}`, {
          signal: AbortSignal.timeout(10000),
        });

        if (hResp.status === 200) {
          const hData = await hResp.json();
          const histEntry = hData[upstreamId];

          if (histEntry) {
            const status = histEntry.status || {};
            const completed = status.completed || status.status_str === 'success';

            if (completed) {
              updatePromptStatus(promptId, 'running', {});

              const outputNodeIds = entry.output_node_ids || [];
              const outputKeys = histEntry.outputs ? Object.keys(histEntry.outputs) : [];
              // suppressed: queue-monitor completed log

              // Find output
              const output = findOutputInHistory(histEntry.outputs, outputNodeIds);
              if (output) {
                try {
                  const saved = await downloadAndSave({
                    serverUrl: server.url,
                    output,
                    workflowId: entry.workflow || promptId,
                    workflowType: entry.prompt_type === 'audio' ? 'audio' : 'image',
                    ext: (output.filename || '').split('.').pop() || 'bin',
                    meta: { params: entry.params || {} },
                  });
                  updatePromptStatus(promptId, 'completed', {
                    file_url: saved.url,
                    file_path: saved.file,
                    terminal_since: Date.now(),
                  });
                  // suppressed: [queue-monitor] COMPLETED
                } catch (dlErr) {
                  // suppressed download error (check pm2 logs if needed)
                  updatePromptStatus(promptId, 'failed', {
                    error: dlErr.message,
                    terminal_since: Date.now(),
                  });
                }
              } else {
                // suppressed: [queue-monitor] no output match
                updatePromptStatus(promptId, 'failed', {
                  error: 'Generation completed but no output file found in history',
                  terminal_since: Date.now(),
                });
              }
            } else if (status.status_str === 'failed' || status.status_str === 'error') {
              updatePromptStatus(promptId, 'failed', {
                terminal_since: Date.now(),
              });
              // suppressed: [queue-monitor] FAILED
            }
          }
        } else if (hResp.status === 404) {
          // Still in queue / waiting, update to running if we see it in queue_remaining
          if (entry.status === 'submitted') {
            updatePromptStatus(promptId, 'running', {});
          }
        } else {
          // suppressed: [queue-monitor] poll status
        }
      } catch (err) {
        // suppressed: [queue-monitor] poll error
      }
    }
  }, 10000);
}

/** @type {Map<string, { subpath: string, expiresAt: number }>} */
export const oneTimeTokens = new Map();

export function newToken() {
  return crypto.randomBytes(24).toString('hex');
}

export function ensureMediaDirs() {
  for (const dir of ['images', 'audio', 'video']) {
    fs.mkdirSync(path.join(MEDIA_DIR, dir), { recursive: true });
  }
}

export function getSequence(dir, ext) {
  try {
    const files = fs.readdirSync(dir).filter((f) => f.endsWith('.' + ext));
    return files.length + 1;
  } catch {
    return 1;
  }
}

export function contentTypeForFile(filePath) {
  const ext = filePath.toLowerCase().split('.').pop() || '';
  if (['mp3', 'm4a', 'aac'].includes(ext)) return 'audio/mpeg';
  if (ext === 'wav') return 'audio/wav';
  if (ext === 'flac') return 'audio/flac';
  if (ext === 'ogg') return 'audio/ogg';
  if (ext === 'png') return 'image/png';
  if (ext === 'jpg' || ext === 'jpeg') return 'image/jpeg';
  if (ext === 'webp') return 'image/webp';
  if (ext === 'mp4') return 'video/mp4';
  return 'application/octet-stream';
}

/**
 * Scan history outputs for first image or audio file.
 * @param {Record<string, object>} outputs
 * @param {string[]} [preferredNodeIds]
 */
export function findOutputInHistory(outputs, preferredNodeIds = []) {
  if (!outputs || typeof outputs !== 'object') return null;

  const normalizedPreferred = preferredNodeIds.map((id) => String(id));

  const tryNode = (nid, out) => {
    const audio = out.audio || [];
    const images = out.images || [];
    if (audio.length > 0) {
      return {
        filename: audio[0].filename,
        subfolder: audio[0].subfolder || '',
        type: audio[0].type || 'output',
        mediaKind: 'audio',
        nodeId: nid,
      };
    }
    if (images.length > 0) {
      return {
        filename: images[0].filename,
        subfolder: images[0].subfolder || '',
        type: images[0].type || 'output',
        mediaKind: 'image',
        nodeId: nid,
      };
    }
    return null;
  };

  for (const nid of normalizedPreferred) {
    if (outputs[nid]) {
      const hit = tryNode(nid, outputs[nid]);
      if (hit) return hit;
    }
  }

  for (const [nid, out] of Object.entries(outputs)) {
    const cleanKey = String(nid).replace(/^(pri|sec)--/, '');
    if (normalizedPreferred.includes(cleanKey) || normalizedPreferred.includes(String(nid))) {
      const hit = tryNode(nid, out);
      if (hit) return hit;
    }
  }

  for (const [nid, out] of Object.entries(outputs)) {
    const hit = tryNode(nid, out);
    if (hit) return hit;
  }
  return null;
}

export async function waitForPrompt(serverUrl, serverPromptId, timeoutMs = 360000) {
  const start = Date.now();
  let lastError = '';
  let consecutiveEmpty200 = 0;

  while (Date.now() - start < timeoutMs) {
    try {
      const hResp = await fetch(`${serverUrl}/history/${serverPromptId}`, {
        signal: AbortSignal.timeout(10000),
      });

      if (hResp.status === 200) {
        const hData = await hResp.json();
        const entry = hData[serverPromptId];

        if (!entry) {
          consecutiveEmpty200++;
          if (consecutiveEmpty200 % 15 === 0) {
            const qResp = await fetch(`${serverUrl}/queue`, { signal: AbortSignal.timeout(5000) });
            const qData = await qResp.json();
            const active = [...(qData.queue_running || []), ...(qData.queue_pending || [])];
            const queued = active.some(
              (item) => Array.isArray(item) && String(item[1]) === String(serverPromptId),
            );
            if (!queued && Date.now() - start > 60000) {
              return { done: true, status: 'cancelled', error: 'Not in queue or history' };
            }
          }
          await new Promise((r) => setTimeout(r, 2000));
          continue;
        }

        consecutiveEmpty200 = 0;
        const status = entry.status || {};
        if (status.completed || status.status_str === 'success') {
          return { done: true, status: 'completed', data: entry };
        }
        if (status.status_str === 'failed' || status.status_str === 'error') {
          const msgs = (status.messages || [])
            .map((m) => m[1]?.toString?.() || '')
            .join('; ');
          return { done: true, status: 'failed', error: msgs || 'Unknown error' };
        }
      } else if (hResp.status === 404) {
        consecutiveEmpty200 = 0;
        const qResp = await fetch(`${serverUrl}/queue`, { signal: AbortSignal.timeout(5000) });
        const qData = await qResp.json();
        const active = [...(qData.queue_running || []), ...(qData.queue_pending || [])];
        const queued = active.some(
          (item) => Array.isArray(item) && String(item[1]) === String(serverPromptId),
        );
        if (!queued && Date.now() - start > 60000) {
          return { done: true, status: 'cancelled', error: 'Not in queue or history after 60s' };
        }
      }
    } catch (err) {
      lastError = err.message || 'connection error';
    }
    await new Promise((r) => setTimeout(r, 2000));
  }
  return {
    done: false,
    status: 'timeout',
    error: `Timeout after ${Math.round((Date.now() - start) / 1000)}s. Last error: ${lastError}`,
  };
}

/**
 * Download output from ComfyUI and save to media directory.
 */
export async function downloadAndSave({
  serverUrl,
  output,
  workflowId,
  workflowType,
  ext,
  meta = {},
}) {
  const subdir = workflowType === 'audio' ? 'audio' : workflowType === 'video' ? 'video' : 'images';
  const mediaDir = path.join(MEDIA_DIR, subdir);
  fs.mkdirSync(mediaDir, { recursive: true });

  const seq = getSequence(mediaDir, ext);
  const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
  const seqPadded = String(seq).padStart(3, '0');

  // Smart naming: Artist - Title_001.ext when params have artist/title
  const artist = meta?.params?.artist;
  const title = meta?.params?.title;
  let outName;
  if (artist && title) {
    const safeArtist = artist.replace(/[/\?%*:|"<>]/g, '_').trim();
    const safeTitle = title.replace(/[/\?%*:|"<>]/g, '_').trim();
    outName = `${safeArtist} - ${safeTitle}_${seqPadded}.${ext}`;
  } else {
    outName = `${workflowId}_${ts}_${seqPadded}.${ext}`;
  }
  const outPath = path.join(mediaDir, outName);

  const viewUrl = new URL(`${serverUrl}/view`);
  viewUrl.searchParams.set('filename', output.filename);
  viewUrl.searchParams.set('subfolder', output.subfolder);
  viewUrl.searchParams.set('type', output.type);

  const dl = await fetch(viewUrl.toString(), { signal: AbortSignal.timeout(60000) });
  if (!dl.ok) {
    const errBody = await dl.text().catch(() => '');
    throw new Error(`Download failed: ${dl.status} - ${errBody.slice(0, 200)}`);
  }
  const buffer = Buffer.from(await dl.arrayBuffer());
  fs.writeFileSync(outPath, buffer);

  const sidecar = {
    workflow: workflowId,
    generated_at: ts,
    file_size: buffer.length,
    ...meta,
  };
  fs.writeFileSync(outPath.replace(`.${ext}`, '.json'), JSON.stringify(sidecar, null, 2));

  return {
    file: outPath,
    filename: outName,
    url: `/media/${subdir}/${outName}`,
    type: workflowType,
    file_size: buffer.length,
  };
}

/**
 * @param {{ type?: string, q?: string, limit?: number }} filters
 */
export function listMedia(filters = {}) {
  const list = { images: [], audio: [], video: [] };
  const typeFilter = filters.type;
  const query = (filters.q || '').toLowerCase();
  const limit = filters.limit ? parseInt(String(filters.limit), 10) : undefined;

  const dirs = typeFilter ? [typeFilter] : ['images', 'audio', 'video'];
  for (const dir of dirs) {
    if (!['images', 'audio', 'video'].includes(dir)) continue;
    const full = path.join(MEDIA_DIR, dir);
    try {
      let files = fs.readdirSync(full).filter((f) => f !== '.gitkeep' && !f.endsWith('.json'));
      if (query) files = files.filter((f) => f.toLowerCase().includes(query));
      files.sort((a, b) => {
        const ta = fs.statSync(path.join(full, a)).mtimeMs;
        const tb = fs.statSync(path.join(full, b)).mtimeMs;
        return tb - ta;
      });
      if (limit) files = files.slice(0, limit);
      list[dir] = files.map((f) => ({
        filename: f,
        url: `/media/${dir}/${f}`,
        size: fs.statSync(path.join(full, f)).size,
        mtime: fs.statSync(path.join(full, f)).mtime.toISOString(),
      }));
    } catch {
      list[dir] = [];
    }
  }
  return list;
}

#!/usr/bin/env node
const fsp = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');

const MEDIA_EXTENSIONS = new Set([
  '.mp4', '.mov', '.m4v', '.mkv', '.avi', '.wmv',
  '.mp3', '.wav', '.aac', '.m4a', '.flac',
  '.jpg', '.jpeg', '.png', '.webp', '.bmp'
]);

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const configPath = path.resolve(args.config || process.env.SKILL_CONFIG || 'config.json');
  const config = await loadConfig(configPath);

  validateConfig(config, [
    'api_base_url',
    'api_key',
    'project_type',
    'aspect_ratio',
    'material_path',
    'template_id',
    'subtitle_mode',
    'music_policy',
    'pace_policy',
    'output_mode',
    'render_preset',
    'timeline_fps',
    'timeline_resolution'
  ]);

  const materials = await scanMaterials(path.resolve(config.material_path));
  if (materials.length === 0) {
    throw new Error(`No supported media files found in ${config.material_path}`);
  }

  const api = new ApiClient(config.api_base_url, config.api_key, config.request_timeout_ms);
  const task = await createTask(api, config, materials, 'davinci-auto-editor');
  const taskId = task.id;

  await api.post(`/v1/tasks/${encodeURIComponent(taskId)}/material-index`, {
    materials,
    summary: buildMaterialSummary(materials)
  });

  const planBundle = await fetchPlanBundle(api, taskId, config, materials);
  const outputDir = resolveOutputDir(config.material_path, taskId);
  await fsp.mkdir(outputDir, { recursive: true });

  const cloudPlan = planBundle.plan || planBundle.data?.plan || planBundle.data || planBundle;
  const importPlan = buildResolveImportPlan(taskId, config, materials, cloudPlan);
  const edlText = renderEdl(importPlan);
  const planPath = path.join(outputDir, 'resolve-import.json');
  const edlPath = path.join(outputDir, 'timeline.edl');
  const guidePath = path.join(outputDir, 'IMPORT-TO-RESOLVE.txt');
  const executionReportPath = path.join(outputDir, 'execution-report.json');

  await writeJson(planPath, importPlan);
  await fsp.writeFile(edlPath, edlText, 'utf8');
  await fsp.writeFile(guidePath, buildImportGuide(importPlan, edlPath), 'utf8');

  const executionReport = {
    taskId,
    executor: 'davinci-auto-editor',
    status: 'prepared',
    generatedAt: new Date().toISOString(),
    outputDir,
    generatedFiles: [planPath, edlPath, guidePath, executionReportPath],
    summary: {
      materialCount: materials.length,
      segmentCount: importPlan.clips.length,
      importFormat: importPlan.importFormat
    }
  };
  await writeJson(executionReportPath, executionReport);
  await api.post(`/v1/tasks/${encodeURIComponent(taskId)}/execute-report`, executionReport);

  console.log(JSON.stringify({
    ok: true,
    taskId,
    outputDir,
    importFormat: importPlan.importFormat,
    generatedFiles: executionReport.generatedFiles
  }, null, 2));
}

function parseArgs(argv) {
  const args = {};
  for (let index = 0; index < argv.length; index += 1) {
    const current = argv[index];
    if (current === '--config') {
      args.config = argv[index + 1];
      index += 1;
      continue;
    }
    if (current === '--help' || current === '-h') {
      printHelp();
      process.exit(0);
    }
  }
  return args;
}

function printHelp() {
  console.log(
    'Usage: node scripts/index.js --config <path-to-config.json>\n\n' +
    'Reads local media, requests a cloud editing plan, and writes a Resolve-importable EDL package.'
  );
}

async function loadConfig(configPath) {
  try {
    const raw = await fsp.readFile(configPath, 'utf8');
    return JSON.parse(raw);
  } catch (error) {
    throw new Error(`Failed to load config at ${configPath}: ${error.message}`);
  }
}

function validateConfig(config, requiredFields) {
  const missing = requiredFields.filter((field) => {
    const value = config[field];
    return value === undefined || value === null || value === '';
  });
  if (missing.length > 0) {
    throw new Error(`Missing required config fields: ${missing.join(', ')}`);
  }
  if (!Number.isFinite(Number(config.timeline_fps)) || Number(config.timeline_fps) <= 0) {
    throw new Error('timeline_fps must be a positive number');
  }
}

async function scanMaterials(rootDir) {
  const rootStats = await fsp.stat(rootDir).catch(() => null);
  if (!rootStats || !rootStats.isDirectory()) {
    throw new Error(`material_path does not exist or is not a directory: ${rootDir}`);
  }

  const results = [];

  async function walk(currentDir) {
    const entries = await fsp.readdir(currentDir, { withFileTypes: true });
    entries.sort((left, right) => left.name.localeCompare(right.name));
    for (const entry of entries) {
      const fullPath = path.join(currentDir, entry.name);
      if (entry.isDirectory()) {
        await walk(fullPath);
        continue;
      }
      const extension = path.extname(entry.name).toLowerCase();
      if (!MEDIA_EXTENSIONS.has(extension)) {
        continue;
      }
      const stats = await fsp.stat(fullPath);
      results.push({
        id: crypto.createHash('sha1').update(fullPath).digest('hex').slice(0, 12),
        name: entry.name,
        extension,
        kind: classifyMedia(extension),
        absolutePath: fullPath,
        relativePath: path.relative(rootDir, fullPath).replace(/\\/g, '/'),
        sizeBytes: stats.size,
        modifiedAt: stats.mtime.toISOString()
      });
    }
  }

  await walk(rootDir);
  return results;
}

function classifyMedia(extension) {
  if (['.mp4', '.mov', '.m4v', '.mkv', '.avi', '.wmv'].includes(extension)) {
    return 'video';
  }
  if (['.mp3', '.wav', '.aac', '.m4a', '.flac'].includes(extension)) {
    return 'audio';
  }
  return 'image';
}

function buildMaterialSummary(materials) {
  const summary = { total: materials.length, video: 0, audio: 0, image: 0 };
  for (const material of materials) {
    summary[material.kind] += 1;
  }
  return summary;
}

class ApiClient {
  constructor(baseUrl, apiKey, timeoutMs = 15000) {
    this.baseUrl = baseUrl.endsWith('/') ? baseUrl : `${baseUrl}/`;
    this.apiKey = apiKey;
    this.timeoutMs = timeoutMs;
  }

  async get(endpoint) {
    return this.request('GET', endpoint);
  }

  async post(endpoint, body) {
    return this.request('POST', endpoint, body);
  }

  async request(method, endpoint, body) {
    const url = new URL(endpoint.replace(/^\//, ''), this.baseUrl);
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeoutMs);
    try {
      const response = await fetch(url, {
        method,
        headers: {
          'content-type': 'application/json',
          'authorization': `Bearer ${this.apiKey}`,
          'user-agent': 'davinci-auto-editor/0.2.0'
        },
        body: body === undefined ? undefined : JSON.stringify(body),
        signal: controller.signal
      });
      const text = await response.text();
      const parsed = text ? JSON.parse(text) : {};
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${parsed.message || text}`);
      }
      return parsed;
    } finally {
      clearTimeout(timer);
    }
  }
}

async function createTask(api, config, materials, executor) {
  const response = await api.post('/v1/tasks/create', {
    executor,
    taskName: config.task_name || `${executor}-${Date.now()}`,
    projectType: config.project_type,
    aspectRatio: config.aspect_ratio,
    templateId: config.template_id,
    outputMode: config.output_mode,
    webhookUrl: config.webhook_url || null,
    extraMetadata: config.extra_metadata || {},
    materialSummary: buildMaterialSummary(materials)
  });

  const task = response.task || response.data?.task || response.data || response;
  if (!task.id) {
    throw new Error('Cloud task creation response did not include task.id');
  }
  return task;
}

async function fetchPlanBundle(api, taskId, config, materials) {
  let response = await api.post(`/v1/tasks/${encodeURIComponent(taskId)}/plan`, {
    projectType: config.project_type,
    aspectRatio: config.aspect_ratio,
    templateId: config.template_id,
    subtitleMode: config.subtitle_mode,
    musicPolicy: config.music_policy,
    pacePolicy: config.pace_policy,
    outputMode: config.output_mode,
    materials
  });

  const status = extractStatus(response);
  if (['queued', 'pending', 'processing'].includes(status)) {
    response = await pollUntilReady(
      api,
      taskId,
      config.task_timeout_ms || 90000,
      config.poll_interval_ms || 1500
    );
  }
  return response;
}

function extractStatus(payload) {
  return payload.status || payload.data?.status || payload.task?.status || 'ready';
}

async function pollUntilReady(api, taskId, timeoutMs, intervalMs) {
  const started = Date.now();
  while (Date.now() - started < timeoutMs) {
    const statusPayload = await api.get(`/v1/tasks/${encodeURIComponent(taskId)}/status`);
    const state = extractStatus(statusPayload);
    if (!['queued', 'pending', 'processing'].includes(state)) {
      return statusPayload.plan
        ? statusPayload
        : { ...statusPayload, plan: statusPayload.plan || statusPayload.data?.plan };
    }
    await sleep(intervalMs);
  }
  throw new Error(`Timed out waiting for task ${taskId} to become ready`);
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function resolveOutputDir(materialPath, taskId) {
  const materialRoot = path.resolve(materialPath);
  return path.join(path.dirname(materialRoot), '_davinci_auto_editor', taskId);
}

function buildResolveImportPlan(taskId, config, materials, cloudPlan) {
  const fps = Number(config.timeline_fps);
  const normalized = normalizeSegments(cloudPlan, materials, fps);
  return {
    taskId,
    executor: 'davinci-auto-editor',
    generatedAt: new Date().toISOString(),
    importFormat: 'cmx3600-edl',
    timeline: {
      name: sanitizeTitle(cloudPlan?.timelineName || config.task_name || `resolve-${taskId}`),
      fps,
      resolution: config.timeline_resolution,
      renderPreset: config.render_preset
    },
    clips: normalized.map((segment, index) => ({
      eventNumber: String(index + 1).padStart(3, '0'),
      reel: buildReelName(segment.material.name, index),
      clipName: segment.material.name,
      sourceFile: segment.material.absolutePath,
      sourceInTc: framesToTimecode(segment.sourceInFrames, fps),
      sourceOutTc: framesToTimecode(segment.sourceOutFrames, fps),
      recordInTc: framesToTimecode(segment.recordInFrames, fps),
      recordOutTc: framesToTimecode(segment.recordOutFrames, fps),
      transition: segment.transition,
      caption: segment.caption
    }))
  };
}

function normalizeSegments(cloudPlan, materials, fps) {
  const byId = new Map(materials.map((material) => [material.id, material]));
  const planSegments = cloudPlan?.segments || cloudPlan?.timeline?.segments || [];
  const timelineMaterials = materials.filter((material) => material.kind !== 'audio');
  const fallbackSource = timelineMaterials.length > 0 ? timelineMaterials : materials;
  const fallbackSegments = fallbackSource.map((material) => ({
    materialId: material.id,
    clipInMs: 0,
    clipOutMs: 5000,
    transition: 'cut',
    caption: ''
  }));
  const rawSegments = Array.isArray(planSegments) && planSegments.length > 0 ? planSegments : fallbackSegments;
  let recordCursorFrames = 0;

  return rawSegments.map((segment, index) => {
    const material =
      byId.get(segment.materialId) ||
      materials.find((item) => item.relativePath === segment.relativePath) ||
      materials[index % materials.length];
    const sourceInFrames = msToFrames(segment.clipInMs ?? 0, fps);
    const requestedOutFrames = msToFrames(segment.clipOutMs ?? 5000, fps);
    const sourceOutFrames = Math.max(sourceInFrames + 1, requestedOutFrames);
    const durationFrames = Math.max(1, sourceOutFrames - sourceInFrames);
    const recordInFrames = recordCursorFrames;
    const recordOutFrames = recordInFrames + durationFrames;
    recordCursorFrames = recordOutFrames;
    return {
      material,
      sourceInFrames,
      sourceOutFrames,
      recordInFrames,
      recordOutFrames,
      transition: segment.transition || 'cut',
      caption: segment.caption || ''
    };
  });
}

function msToFrames(ms, fps) {
  return Math.max(0, Math.round((Number(ms) / 1000) * fps));
}

function framesToTimecode(totalFrames, fps) {
  const roundedFps = Math.round(fps);
  const frames = totalFrames % roundedFps;
  const totalSeconds = Math.floor(totalFrames / roundedFps);
  const seconds = totalSeconds % 60;
  const totalMinutes = Math.floor(totalSeconds / 60);
  const minutes = totalMinutes % 60;
  const hours = Math.floor(totalMinutes / 60);
  return [hours, minutes, seconds, frames].map((value) => String(value).padStart(2, '0')).join(':');
}

function buildReelName(fileName, index) {
  const stem = path.parse(fileName).name.toUpperCase().replace(/[^A-Z0-9]/g, '');
  const candidate = stem.slice(0, 8);
  if (candidate.length > 0) {
    return candidate.padEnd(8, 'X');
  }
  return `REEL${String(index + 1).padStart(4, '0')}`.slice(0, 8);
}

function sanitizeTitle(value) {
  return String(value).replace(/[^\w\- ]+/g, '').slice(0, 64) || 'Resolve Auto Timeline';
}

function renderEdl(importPlan) {
  const lines = [
    `TITLE: ${importPlan.timeline.name}`,
    'FCM: NON-DROP FRAME',
    ''
  ];

  for (const clip of importPlan.clips) {
    lines.push(
      `${clip.eventNumber}  ${clip.reel} V     C        ${clip.sourceInTc} ${clip.sourceOutTc} ${clip.recordInTc} ${clip.recordOutTc}`
    );
    lines.push(`* FROM CLIP NAME: ${clip.clipName}`);
    lines.push(`* SOURCE FILE: ${clip.sourceFile}`);
    if (clip.caption) {
      lines.push(`* COMMENT: ${clip.caption}`);
    }
  }

  lines.push('');
  return `${lines.join('\n')}\n`;
}

function buildImportGuide(importPlan, edlPath) {
  return [
    `DaVinci Resolve import package for task ${importPlan.taskId}`,
    '',
    '1. Open DaVinci Resolve and create or open a project.',
    '2. Import the source clips into the Media Pool before importing the timeline.',
    `3. Import the EDL file: ${edlPath}`,
    '4. If Resolve asks for clip relinking, point it to the scanned material folder.',
    `5. Timeline FPS: ${importPlan.timeline.fps}`,
    `6. Timeline resolution: ${importPlan.timeline.resolution}`,
    `7. Suggested render preset: ${importPlan.timeline.renderPreset}`,
    '',
    'This package intentionally contains only the minimum local execution data and does not include the full cloud plan.'
  ].join('\n');
}

async function loadJson(filePath) {
  const raw = await fsp.readFile(filePath, 'utf8');
  return JSON.parse(raw);
}

async function writeJson(targetPath, payload) {
  await fsp.writeFile(targetPath, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
}

main().catch(async (error) => {
  const payload = {
    ok: false,
    error: error.message,
    stack: error.stack,
    generatedAt: new Date().toISOString()
  };
  try {
    const configArg = parseArgs(process.argv.slice(2)).config;
    if (configArg) {
      const config = await loadConfig(path.resolve(configArg));
      if (config.material_path) {
        const fallbackDir = resolveOutputDir(config.material_path, 'failed-task');
        await fsp.mkdir(fallbackDir, { recursive: true });
        await writeJson(path.join(fallbackDir, 'execution-report.json'), payload);
      }
    }
  } catch (_) {
    // Best effort only.
  }
  console.error(payload.error);
  process.exit(1);
});

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
export const PROJECT_ROOT = path.resolve(__dirname, '..');
export const WORKFLOW_DIR = path.join(PROJECT_ROOT, 'workflows');
export const REGISTRY_PATH = path.join(PROJECT_ROOT, 'workflows-registry.json');

// Empty defaults for public repo
const LEGACY_WORKFLOW_DEFAULTS = {};

/** @type {Record<string, object>} */
let registry = {};

function nowIso() {
  return new Date().toISOString();
}

function loadRegistryFile() {
  if (!fs.existsSync(REGISTRY_PATH)) {
    registry = {};
    return;
  }
  try {
    const raw = JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf-8'));
    registry = raw.workflows && typeof raw.workflows === 'object' ? raw.workflows : raw;
  } catch (err) {
    console.error(`Failed to load registry: ${err.message}`);
    registry = {};
  }
}

function saveRegistryFile() {
  const payload = { version: 1, updated_at: nowIso(), workflows: registry };
  fs.writeFileSync(REGISTRY_PATH, JSON.stringify(payload, null, 2));
}

function slugFromFilename(filename) {
  return filename.replace(/\.json$/i, '');
}

function defaultEntryForFile(filename) {
  const id = slugFromFilename(filename);
  const ts = nowIso();
  return {
    id,
    title: id.replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase()),
    description: `Auto-registered workflow from ${filename}`,
    type: 'other',
    file: filename,
    ext: 'png',
    created_at: ts,
    updated_at: ts,
    editable_params: [],
    output_node_ids: [],
    submit_config: {
      client_id_generation: 'auto',
      preserve_seed: true,
      validation_schema: {},
    },
  };
}

/**
 * Scan workflows/ and register any missing JSON files.
 */
export function migrateFromDisk() {
  loadRegistryFile();
  if (!fs.existsSync(WORKFLOW_DIR)) {
    fs.mkdirSync(WORKFLOW_DIR, { recursive: true });
  }

  const files = fs.readdirSync(WORKFLOW_DIR).filter((f) => f.endsWith('.json'));
  let added = 0;

  for (const file of files) {
    const id = slugFromFilename(file);
    if (registry[id]) continue;

    if (LEGACY_WORKFLOW_DEFAULTS[id]) {
      const ts = nowIso();
      registry[id] = {
        ...LEGACY_WORKFLOW_DEFAULTS[id],
        created_at: ts,
        updated_at: ts,
      };
    } else {
      registry[id] = defaultEntryForFile(file);
    }
    added++;
    console.log(`Registry: auto-registered workflow "${id}" from ${file}`);
  }

  if (added > 0 || !fs.existsSync(REGISTRY_PATH)) {
    saveRegistryFile();
  }
}

export function initRegistry() {
  migrateFromDisk();
  return registry;
}

export function listWorkflowsMeta() {
  const list = {};
  for (const [id, w] of Object.entries(registry)) {
    list[id] = {
      id: w.id,
      title: w.title,
      type: w.type,
      ext: w.ext,
      description: w.description,
      file: w.file,
      updated_at: w.updated_at,
    };
  }
  return list;
}

export function getWorkflow(id) {
  return registry[id] || null;
}

export function createWorkflow(entry) {
  const id = entry.id;
  if (!id || registry[id]) {
    throw new Error(registry[id] ? 'Workflow id already exists' : 'id is required');
  }
  const ts = nowIso();
  registry[id] = {
    ...entry,
    created_at: ts,
    updated_at: ts,
  };
  saveRegistryFile();
  return registry[id];
}

export function updateWorkflow(id, patch) {
  const existing = registry[id];
  if (!existing) return null;
  registry[id] = {
    ...existing,
    ...patch,
    id,
    updated_at: nowIso(),
  };
  saveRegistryFile();
  return registry[id];
}

export function deleteWorkflow(id) {
  const existing = registry[id];
  if (!existing) return null;
  if (existing.file) {
    const wfPath = path.join(WORKFLOW_DIR, existing.file);
    if (fs.existsSync(wfPath)) fs.unlinkSync(wfPath);
  }
  delete registry[id];
  saveRegistryFile();
  return existing;
}

export function loadWorkflowJson(id) {
  const meta = registry[id];
  if (!meta) return null;
  const wfPath = path.join(WORKFLOW_DIR, meta.file);
  if (!fs.existsSync(wfPath)) return null;
  return JSON.parse(fs.readFileSync(wfPath, 'utf-8'));
}

export function saveWorkflowJsonFile(id, jsonContent) {
  const meta = registry[id];
  if (!meta) throw new Error('Unknown workflow');
  const wfPath = path.join(WORKFLOW_DIR, meta.file);
  const data = typeof jsonContent === 'string' ? jsonContent : JSON.stringify(jsonContent, null, 2);
  fs.writeFileSync(wfPath, data);
  meta.updated_at = nowIso();
  saveRegistryFile();
}

export function previewSchema(id) {
  const w = registry[id];
  if (!w) return null;
  return {
    id: w.id,
    title: w.title,
    description: w.description,
    type: w.type,
    ext: w.ext,
    fields: (w.editable_params || []).map((p) => ({
      nodeId: p.nodeId,
      field: p.field,
      label: p.label,
      type: p.type,
      required: !!p.required,
      default: p.default,
      options: p.options,
      description: p.description,
      paramKey: p.paramKey || p.field,
    })),
    output_node_ids: w.output_node_ids || [],
    submit_config: w.submit_config || {},
  };
}

/**
 * Apply request params onto workflow JSON using editable_params definitions.
 */
export function applyParamsToWorkflow(wf, meta, params) {
  const body = { ...params };
  if (body.prompt === undefined && body.text !== undefined) body.prompt = body.text;

  for (const p of meta.editable_params || []) {
    const key = p.paramKey || p.field;
    let value = body[key];
    if (value === undefined && body[p.field] !== undefined) value = body[p.field];

    if (p.required && (value === undefined || value === null || value === '')) {
      throw new Error(`Missing required param: ${key} (${p.label})`);
    }
    if (value === undefined) continue;

    const node = wf[p.nodeId];
    if (!node?.inputs) continue;
    node.inputs[p.field] = value;

    if (p.mirrorNodes) {
      for (const mid of p.mirrorNodes) {
        if (wf[mid]?.inputs) wf[mid].inputs[p.field] = value;
      }
    }
  }

  return wf;
}

/* === Workflow Import/Conversion === */

/**
 * Detect if a JSON object is a non-API ComfyUI workflow (exported from UI).
 */
export function isNonApiWorkflow(json) {
  return json && typeof json === 'object' && Array.isArray(json.nodes) && json.nodes.length > 0;
}

/**
 * Convert a non-API ComfyUI workflow JSON to API-friendly format.
 */
export function convertNonApiToApi(json) {
  if (!isNonApiWorkflow(json)) return json;

  const { nodes, links } = json;
  const linkMap = {};

  if (Array.isArray(links)) {
    for (const link of links) {
      const [linkId, srcId, srcSlot, tgtId, tgtSlot] = link;
      linkMap[linkId] = { srcId: String(srcId), srcSlot, tgtId: String(tgtId), tgtSlot };
    }
  }

  const apiWorkflow = {};

  for (const node of nodes) {
    const nodeId = String(node.id);
    const classType = node.type;
    const inputs = {};

    if (Array.isArray(node.inputs)) {
      for (let i = 0; i < node.inputs.length; i++) {
        const inp = node.inputs[i];
        const fieldName = inp.name;

        if (inp.link !== null && inp.link !== undefined && linkMap[inp.link]) {
          const conn = linkMap[inp.link];
          inputs[fieldName] = [conn.srcId, conn.srcSlot];
        } else {
          const widgetVal = node.widgets_values?.[i];
          if (widgetVal !== undefined && widgetVal !== null) {
            inputs[fieldName] = widgetVal;
          }
        }
      }
    }

    apiWorkflow[nodeId] = { class_type: classType, inputs };
  }

  return apiWorkflow;
}

/**
 * Import a workflow JSON (API or non-API) and register it as a runnable workflow.
 */
export function importWorkflow(id, jsonContent, meta = {}) {
  const apiWorkflow = isNonApiWorkflow(jsonContent) ? convertNonApiToApi(jsonContent) : jsonContent;

  let type = meta.type || 'other';
  let ext = meta.ext || 'png';

  if (!meta.type || meta.type === 'other') {
    const nodeValues = Object.values(apiWorkflow);
    const classTypes = nodeValues.map(n => n.class_type || '');
    const hasAudio = classTypes.some(ct => ct.toLowerCase().includes('audio') || ct.toLowerCase().includes('ace'));
    const hasImage = classTypes.some(ct => ct.toLowerCase().includes('vae') || ct.toLowerCase().includes('ksampler') || ct.toLowerCase().includes('latent') || ct.toLowerCase().includes('image'));

    if (hasAudio) { type = 'audio'; ext = 'mp3'; }
    else if (hasImage) { type = 'image'; ext = 'png'; }
  }

  const existing = registry[id];
  const ts = nowIso();

  if (existing) {
    registry[id] = { ...existing, ...meta, id, type: type || existing.type, ext: ext || existing.ext, updated_at: ts };
  } else {
    registry[id] = {
      id,
      title: meta.title || id.replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase()),
      description: meta.description || `Imported workflow: ${id}`,
      type, ext, file: `${id}.json`, created_at: ts, updated_at: ts,
      editable_params: [], output_node_ids: [],
      submit_config: { client_id_generation: 'auto', preserve_seed: true, validation_schema: {} },
    };
  }

  const wfPath = path.join(WORKFLOW_DIR, `${id}.json`);
  fs.writeFileSync(wfPath, JSON.stringify(apiWorkflow, null, 2));
  saveRegistryFile();

  return registry[id];
}
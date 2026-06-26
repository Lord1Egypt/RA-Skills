import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { Sandbox } from 'e2b';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const SKILL_DIR = path.resolve(__dirname, '..');
const WORKSPACE_DIR = path.resolve(SKILL_DIR, '..', '..');
const STATE_DIR = path.join(WORKSPACE_DIR, '.state');
const STATE_PATH = path.join(STATE_DIR, 'e2b-sandboxes.json');

function ensureStateDir() {
  fs.mkdirSync(STATE_DIR, { recursive: true });
}

export function loadState() {
  try {
    return JSON.parse(fs.readFileSync(STATE_PATH, 'utf8'));
  } catch {
    return { sandboxes: [] };
  }
}

export function saveState(state) {
  ensureStateDir();
  fs.writeFileSync(STATE_PATH, JSON.stringify(state, null, 2));
}

export function upsertRecord(record) {
  const state = loadState();
  const sandboxes = Array.isArray(state.sandboxes) ? state.sandboxes : [];
  const next = sandboxes.filter((item) => item.sandboxId !== record.sandboxId);
  next.push(record);
  saveState({ sandboxes: next.sort((a, b) => String(a.createdAt).localeCompare(String(b.createdAt))) });
}

export function removeRecord(sandboxId) {
  const state = loadState();
  const sandboxes = Array.isArray(state.sandboxes) ? state.sandboxes : [];
  saveState({ sandboxes: sandboxes.filter((item) => item.sandboxId !== sandboxId) });
}

export function findRecord(ref) {
  const state = loadState();
  const sandboxes = Array.isArray(state.sandboxes) ? state.sandboxes : [];
  const byId = sandboxes.find((item) => item.sandboxId === ref);
  if (byId) return byId;
  const byLabel = sandboxes.filter((item) => item.label === ref);
  if (byLabel.length === 1) return byLabel[0];
  if (byLabel.length > 1) throw new Error(`Sandbox label '${ref}' is ambiguous. Use the sandbox id instead.`);
  return null;
}

export function resolveSandboxRef(ref) {
  if (!ref) throw new Error('Missing sandbox id or label');
  const record = findRecord(ref);
  return { sandboxId: record?.sandboxId ?? ref, record };
}

export async function connectSandbox(ref) {
  const { sandboxId, record } = resolveSandboxRef(ref);
  const sandbox = await Sandbox.connect(sandboxId);
  return { sandbox, sandboxId, record };
}

export async function createSandbox({ label = null, template = 'base', timeoutMs = 3_600_000, envs = {}, metadata = {} } = {}) {
  const sandbox = await Sandbox.create({
    template,
    timeoutMs,
    envs: Object.keys(envs).length ? envs : undefined,
    metadata: {
      createdBy: 'openclaw-e2b-skill',
      ...(label ? { label } : {}),
      ...metadata,
    },
  });
  const info = await sandbox.getInfo();
  const record = {
    sandboxId: sandbox.sandboxId,
    label,
    template,
    timeoutMs,
    createdAt: new Date().toISOString(),
    metadata: info.metadata ?? {},
  };
  upsertRecord(record);
  return {
    ok: true,
    ...record,
    info,
    sandboxHostHint: `https://3000-${sandbox.sandboxId}.e2b.app`,
  };
}

export async function listSandboxes() {
  const state = loadState();
  return {
    ok: true,
    statePath: STATE_PATH,
    sandboxes: Array.isArray(state.sandboxes) ? state.sandboxes : [],
  };
}

export async function getSandboxInfo({ sandbox: ref }) {
  const { sandbox, sandboxId, record } = await connectSandbox(ref);
  const info = await sandbox.getInfo();
  upsertRecord({
    sandboxId,
    label: record?.label ?? info.metadata?.label ?? null,
    template: info.name ?? record?.template ?? null,
    timeoutMs: record?.timeoutMs ?? null,
    createdAt: record?.createdAt ?? new Date().toISOString(),
    metadata: info.metadata ?? {},
  });
  return { ok: true, sandboxId, record: record ?? null, info };
}

export async function execInSandbox({ sandbox: ref, cmd, cwd, envs = {}, timeoutMs }) {
  if (!cmd) throw new Error('Missing cmd');
  const { sandbox, sandboxId } = await connectSandbox(ref);
  const result = await sandbox.commands.run(cmd, {
    cwd,
    envs: Object.keys(envs).length ? envs : undefined,
    timeoutMs,
  });
  return {
    ok: true,
    sandboxId,
    command: cmd,
    cwd: cwd ?? null,
    stdout: result.stdout ?? '',
    stderr: result.stderr ?? '',
    exitCode: result.exitCode ?? null,
  };
}

export async function getSandboxHost({ sandbox: ref, port }) {
  const { sandbox, sandboxId, record } = await connectSandbox(ref);
  const host = sandbox.getHost(port);
  return { ok: true, sandboxId, label: record?.label ?? null, port, host };
}

export async function setSandboxTimeout({ sandbox: ref, timeoutMs }) {
  const { sandbox, sandboxId, record } = await connectSandbox(ref);
  await sandbox.setTimeout(timeoutMs);
  if (record) upsertRecord({ ...record, timeoutMs });
  return { ok: true, sandboxId, timeoutMs };
}

export async function snapshotSandbox({ sandbox: ref }) {
  const { sandbox, sandboxId } = await connectSandbox(ref);
  const snapshot = await sandbox.createSnapshot();
  return { ok: true, sandboxId, snapshot };
}

export async function killSandbox({ sandbox: ref }) {
  const { sandbox, sandboxId } = await connectSandbox(ref);
  await sandbox.kill();
  removeRecord(sandboxId);
  return { ok: true, sandboxId, killed: true };
}

export { STATE_PATH, SKILL_DIR, WORKSPACE_DIR };

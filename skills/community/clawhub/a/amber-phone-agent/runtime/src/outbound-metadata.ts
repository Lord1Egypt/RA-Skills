import { randomUUID } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

export const OUTBOUND_INTENT_RETENTION_MS = 10 * 60 * 1000;

export interface OutboundMetadata<Plan> {
  bridgeId?: string;
  to?: string;
  objective?: string | null;
  callPlan?: Plan | null;
  model?: string;
  createdAtMs: number;
}

type StoredOutboundMetadata<Plan> = {
  schema: 1;
  updatedAt: string;
  calls: Record<string, OutboundMetadata<Plan>>;
};

export function freshOutboundIntent(createdAtMs: number, now: number): boolean {
  const age = now - createdAtMs;
  return age >= 0 && age < OUTBOUND_INTENT_RETENTION_MS;
}

// Accept the dashboard format along with the older flat restart file.
function readOutboundMetadata<Plan>(file: string): StoredOutboundMetadata<Plan> {
  try {
    const fd = fs.openSync(file, fs.constants.O_RDONLY | fs.constants.O_NONBLOCK);
    try {
      const status = fs.fstatSync(fd);
      if (!status.isFile()) throw new Error('Outbound metadata must be a regular file');
      if ((status.mode & 0o777) !== 0o600) fs.fchmodSync(fd, 0o600);
      const payload = JSON.parse(fs.readFileSync(fd, 'utf8'));
      const calls = payload?.calls ?? payload;
      if (!calls || typeof calls !== 'object' || Array.isArray(calls)) {
        throw new SyntaxError('Invalid outbound metadata file');
      }
      return {
        schema: 1,
        updatedAt: payload.updatedAt,
        calls: Object.assign(Object.create(null), calls),
      };
    } finally {
      fs.closeSync(fd);
    }
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code !== 'ENOENT') throw error;
    return { schema: 1, updatedAt: '', calls: Object.create(null) };
  }
}

export function updateOutboundMetadata<Plan>(
  file: string,
  now: number,
  call?: { sid: string; metadata: OutboundMetadata<Plan> },
): Record<string, OutboundMetadata<Plan>> {
  let stored: StoredOutboundMetadata<Plan>;
  try {
    stored = readOutboundMetadata<Plan>(file);
  } catch (error) {
    if (!call || !(error instanceof SyntaxError)) throw error;
    stored = { schema: 1, updatedAt: '', calls: Object.create(null) };
  }
  let changed = Boolean(call);
  if (call) stored.calls[call.sid] = call.metadata;
  for (const [id, item] of Object.entries(stored.calls)) {
    if (!item || typeof item !== 'object' || !Number.isFinite(item.createdAtMs)) {
      delete stored.calls[id];
      changed = true;
      continue;
    }
    if (!freshOutboundIntent(item.createdAtMs, now) && 'callPlan' in item) {
      // The dashboard needs the routing and objective history. Structured
      // customer details only need to survive long enough to connect the call.
      delete item.callPlan;
      changed = true;
    }
  }
  if (changed) {
    const dir = path.dirname(file);
    fs.mkdirSync(dir, { recursive: true });
    const temporary = path.join(dir, `.${path.basename(file)}.${randomUUID()}.tmp`);
    try {
      stored.updatedAt = new Date(now).toISOString();
      fs.writeFileSync(temporary, JSON.stringify(stored, null, 2) + '\n', { flag: 'wx', mode: 0o600 });
      fs.renameSync(temporary, file);
    } finally {
      fs.rmSync(temporary, { force: true });
    }
  }
  return stored.calls;
}

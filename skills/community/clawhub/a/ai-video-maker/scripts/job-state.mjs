import { createHash, randomUUID } from "node:crypto";
import { constants } from "node:fs";
import { open, rename, rm } from "node:fs/promises";
import { resolve } from "node:path";

// Canonical object order makes equivalent JSON payloads share a recovery identity.
function canonical(value) {
  if (Array.isArray(value)) return value.map(canonical);
  if (value && typeof value === "object")
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .map((key) => [key, canonical(value[key])]),
    );
  return value;
}

export async function readJobState(path) {
  const handle = await open(resolve(path), constants.O_RDONLY | constants.O_NOFOLLOW);
  try {
    const state = JSON.parse(await handle.readFile("utf8"));
    if (state.version !== 1 || typeof state.idempotencyKey !== "string")
      throw new Error("Invalid recovery state. Preserve it and inspect the original task.");
    return state;
  } finally {
    await handle.close();
  }
}

export async function prepareJobState(path, { model, payload, maxCredits, idempotencyKey }) {
  const fingerprint = createHash("sha256")
    .update(JSON.stringify(canonical({ model, payload, maxCredits })))
    .digest("hex");
  const state = {
    version: 1,
    model,
    fingerprint,
    maxCredits,
    idempotencyKey: idempotencyKey || randomUUID(),
    createdAt: new Date().toISOString(),
  };
  try {
    const handle = await open(resolve(path), "wx", 0o600);
    try {
      await handle.writeFile(`${JSON.stringify(state, null, 2)}\n`);
      await handle.sync();
    } finally {
      await handle.close();
    }
    return state;
  } catch (error) {
    if (error.code !== "EEXIST") throw error;
  }
  const saved = await readJobState(path);
  if (
    saved.fingerprint !== fingerprint ||
    (idempotencyKey && saved.idempotencyKey !== idempotencyKey)
  )
    throw new Error(
      "Recovery state belongs to a different request or budget. Do not overwrite it.",
    );
  return saved;
}

export async function saveTaskId(path, state, taskId) {
  const temporary = `${resolve(path)}.${randomUUID()}.tmp`;
  try {
    const handle = await open(temporary, "wx", 0o600);
    try {
      await handle.writeFile(`${JSON.stringify({ ...state, taskId }, null, 2)}\n`);
      await handle.sync();
    } finally {
      await handle.close();
    }
    await rename(temporary, resolve(path));
  } finally {
    await rm(temporary, { force: true });
  }
}

import fs from "node:fs/promises";
import path from "node:path";

async function readJsonFile(filePath, fallbackValue = null) {
  try {
    return JSON.parse(await fs.readFile(filePath, "utf8"));
  } catch (error) {
    if (error && typeof error === "object" && "code" in error && error.code === "ENOENT") {
      return fallbackValue;
    }

    throw error;
  }
}

async function writeJsonFile(filePath, value) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

export function timestampValue(value) {
  const parsed = Date.parse(value ?? "");
  return Number.isFinite(parsed) ? parsed : 0;
}

export function compareTimeline(left, right, fallbackKeys = []) {
  const createdDelta = timestampValue(left?.createdAt) - timestampValue(right?.createdAt);

  if (createdDelta !== 0) {
    return createdDelta;
  }

  const updatedDelta = timestampValue(left?.updatedAt) - timestampValue(right?.updatedAt);

  if (updatedDelta !== 0) {
    return updatedDelta;
  }

  for (const key of fallbackKeys) {
    const compare = String(left?.[key] ?? "").localeCompare(String(right?.[key] ?? ""));

    if (compare !== 0) {
      return compare;
    }
  }

  return 0;
}

export function sortTimeline(records, fallbackKeys = []) {
  return [...records].sort((left, right) => compareTimeline(left, right, fallbackKeys));
}

export function appendMapValue(map, key, value) {
  const current = map.get(key) ?? [];
  current.push(value);
  map.set(key, current);
}

export async function updateJsonFile(filePath, fallbackValue, updater) {
  const current = await readJsonFile(filePath, structuredClone(fallbackValue));
  const draft = structuredClone(current);
  const nextValue = updater(draft) ?? draft;

  await writeJsonFile(filePath, nextValue);
  return nextValue;
}

export async function readJsonRecords(directoryPath) {
  let entries;

  try {
    entries = await fs.readdir(directoryPath, { withFileTypes: true });
  } catch (error) {
    if (error && typeof error === "object" && "code" in error && error.code === "ENOENT") {
      return [];
    }

    throw error;
  }

  const records = [];

  for (const entry of entries) {
    if (!entry.isFile() || !entry.name.endsWith(".json")) {
      continue;
    }

    const record = await readJsonFile(path.join(directoryPath, entry.name), null);
    if (record) {
      records.push(record);
    }
  }

  return records;
}

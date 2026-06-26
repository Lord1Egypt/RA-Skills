import fs from 'node:fs/promises';
import path from 'node:path';

export const TWO_WEEKS_MS = 14 * 24 * 60 * 60 * 1000;

export function parseArgs(argv = process.argv.slice(2)) {
  const args = {};
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith('--')) {
      if (!Array.isArray(args._)) args._ = [];
      args._.push(token);
      continue;
    }

    const rawKey = token.slice(2);
    if (rawKey.includes('=')) {
      const [key, ...rest] = rawKey.split('=');
      args[key] = rest.join('=');
      continue;
    }

    const next = argv[index + 1];
    if (!next || next.startsWith('--')) {
      args[rawKey] = true;
      continue;
    }

    args[rawKey] = next;
    index += 1;
  }
  return args;
}

export function asBoolean(value, fallback = false) {
  if (value === undefined || value === null) return fallback;
  if (typeof value === 'boolean') return value;
  const normalized = String(value).trim().toLowerCase();
  if (['1', 'true', 'yes', 'on'].includes(normalized)) return true;
  if (['0', 'false', 'no', 'off'].includes(normalized)) return false;
  return fallback;
}

export function asInteger(value, fallback) {
  if (value === undefined || value === null || value === '') return fallback;
  const parsed = Number.parseInt(String(value), 10);
  if (Number.isNaN(parsed)) return fallback;
  return parsed;
}

export function parseDateToTs(value, fallback = undefined) {
  if (!value) return fallback;
  const timestamp = Date.parse(value);
  if (Number.isNaN(timestamp)) {
    throw new Error(`Invalid date value: ${value}`);
  }
  return timestamp;
}

export function requireArg(args, key, message) {
  const value = args[key];
  if (value === undefined || value === null || value === '') {
    throw new Error(message ?? `Missing required argument --${key}`);
  }
  return String(value);
}

export function resolveToken(args) {
  const value = args.token || process.env.DISCORD_BOT_TOKEN;
  if (!value) {
    throw new Error('Missing Discord token. Provide --token or DISCORD_BOT_TOKEN.');
  }
  return String(value).trim();
}

export function normalizeToken(token) {
  return token.startsWith('Bot ') ? token : `Bot ${token}`;
}

export async function sleep(milliseconds) {
  const duration = Math.max(0, Number(milliseconds) || 0);
  if (duration === 0) return;
  await new Promise((resolve) => setTimeout(resolve, duration));
}

export function chunkList(input, size) {
  const chunkSize = Math.max(1, size);
  const output = [];
  for (let start = 0; start < input.length; start += chunkSize) {
    output.push(input.slice(start, start + chunkSize));
  }
  return output;
}

export function sanitizeObject(input) {
  return Object.fromEntries(
    Object.entries(input).filter(([, value]) => value !== undefined)
  );
}

export function isOlderThanTwoWeeks(messageTimestamp, nowTs = Date.now()) {
  return nowTs - Date.parse(messageTimestamp) > TWO_WEEKS_MS;
}

export async function writeJson(filePath, data) {
  const outputPath = path.resolve(filePath);
  await fs.mkdir(path.dirname(outputPath), { recursive: true });
  await fs.writeFile(outputPath, JSON.stringify(data, null, 2), 'utf8');
}

export function printJson(data) {
  process.stdout.write(`${JSON.stringify(data, null, 2)}\n`);
}

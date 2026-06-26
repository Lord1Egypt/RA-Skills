import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { execFile as execFileCallback } from "node:child_process";
import { promisify } from "node:util";

const execFile = promisify(execFileCallback);

export const SHORT_SLEEP_HOURS = 6;
export const HIGH_RISK_SLEEP_HOURS = 5;

export function formatLocalIso(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const hours = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");
  const seconds = String(date.getSeconds()).padStart(2, "0");
  const offsetMinutes = -date.getTimezoneOffset();
  const sign = offsetMinutes >= 0 ? "+" : "-";
  const absMinutes = Math.abs(offsetMinutes);
  const offsetHours = String(Math.floor(absMinutes / 60)).padStart(2, "0");
  const offsetRemainder = String(absMinutes % 60).padStart(2, "0");

  return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}${sign}${offsetHours}:${offsetRemainder}`;
}

export function getLocalDateKey(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

export function startOfLocalDay(date) {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate(), 0, 0, 0, 0);
}

export function addDays(date, days) {
  const next = new Date(date);
  next.setDate(next.getDate() + days);
  return next;
}

export function diffHours(start, end) {
  return Number(((end.getTime() - start.getTime()) / 3_600_000).toFixed(1));
}

export function average(values) {
  if (values.length === 0) {
    return null;
  }

  const total = values.reduce((sum, value) => sum + value, 0);
  return Number((total / values.length).toFixed(1));
}

export function longestConsecutive(values, predicate) {
  let longest = 0;
  let current = 0;

  for (const value of values) {
    if (predicate(value)) {
      current += 1;
      longest = Math.max(longest, current);
      continue;
    }

    current = 0;
  }

  return longest;
}

export async function ensureDirectory(targetDir) {
  await fs.mkdir(targetDir, { recursive: true });
}

export async function writeJsonFile(targetFile, data) {
  const directory = path.dirname(targetFile);
  await ensureDirectory(directory);
  await fs.writeFile(targetFile, JSON.stringify(data, null, 2) + "\n", "utf8");
}

export function dontDealHome(env = process.env) {
  if (env.DONT_DEAL_HOME) {
    return path.resolve(env.DONT_DEAL_HOME);
  }

  return path.join(os.homedir(), ".dont-deal");
}

export async function pathExists(targetPath) {
  try {
    await fs.access(targetPath);
    return true;
  } catch {
    return false;
  }
}

export async function runCommand(command, args, options = {}) {
  const { stdout, stderr } = await execFile(command, args, {
    encoding: "utf8",
    ...options
  });

  return {
    stdout: stdout.trim(),
    stderr: stderr.trim()
  };
}

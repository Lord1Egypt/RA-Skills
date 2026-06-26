import crypto from "node:crypto";

export function sha256(value) {
  return crypto.createHash("sha256").update(value).digest("hex");
}

export function sanitizeFilePart(value) {
  return String(value).replace(/[^a-zA-Z0-9._-]+/g, "-").replace(/^-+|-+$/g, "") || "item";
}

export function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export function nowIso() {
  return new Date().toISOString();
}

export function createTimestampSlug(date = new Date()) {
  return date.toISOString().replace(/[:.]/g, "-");
}

export function splitLocalDateTime(value) {
  const match = String(value).trim().replace("T", " ").match(/^(\d{4}-\d{2}-\d{2}) (\d{2}):(\d{2})$/);
  if (!match) {
    throw new Error(`Invalid local datetime: ${value}`);
  }

  return {
    date: match[1],
    hour: match[2],
    minute: match[3],
    time: `${match[2]}:${match[3]}`
  };
}

export function parseLocalDateTime(value) {
  const parts = splitLocalDateTime(value);
  const [year, month, day] = parts.date.split("-").map(Number);
  const hour = Number(parts.hour);
  const minute = Number(parts.minute);

  return new Date(Date.UTC(year, month - 1, day, hour - 8, minute));
}

export function formatLocalDateTime(date) {
  const localDate = new Date(date.getTime() + 8 * 60 * 60 * 1000);
  const year = localDate.getUTCFullYear();
  const month = String(localDate.getUTCMonth() + 1).padStart(2, "0");
  const day = String(localDate.getUTCDate()).padStart(2, "0");
  const hour = String(localDate.getUTCHours()).padStart(2, "0");
  const minute = String(localDate.getUTCMinutes()).padStart(2, "0");

  return `${year}-${month}-${day} ${hour}:${minute}`;
}

export function addDaysToLocalDateTime(value, days) {
  const date = parseLocalDateTime(value);
  return formatLocalDateTime(new Date(date.getTime() + days * 24 * 60 * 60 * 1000));
}

export function getLocalDurationMinutes(startValue, endValue) {
  const start = parseLocalDateTime(startValue);
  const end = parseLocalDateTime(endValue);
  return Math.round((end.getTime() - start.getTime()) / (60 * 1000));
}

export function formatDurationMinutes(value) {
  const totalMinutes = Math.max(0, Number(value) || 0);
  const days = Math.floor(totalMinutes / (24 * 60));
  const hours = Math.floor((totalMinutes % (24 * 60)) / 60);
  const minutes = totalMinutes % 60;
  const parts = [];

  if (days) {
    parts.push(`${days}天`);
  }
  if (hours) {
    parts.push(`${hours}小时`);
  }
  if (minutes || parts.length === 0) {
    parts.push(`${minutes}分`);
  }

  return parts.join("");
}

export function safeNumber(value) {
  if (value === null || value === undefined || value === "") {
    return null;
  }

  const number = Number(value);
  return Number.isFinite(number) ? number : null;
}

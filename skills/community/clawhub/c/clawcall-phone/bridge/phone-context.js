"use strict";

const fs = require("fs");
const path = require("path");
const { execFile } = require("child_process");

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.resolve(__dirname, "..", "..", "..");

function readTextSafe(filePath) {
  try {
    return fs.readFileSync(filePath, "utf8");
  } catch {
    return "";
  }
}

function compact(text, maxChars) {
  const clean = (text || "").replace(/\r/g, "").trim();
  if (!clean) return "";
  return clean.length <= maxChars ? clean : clean.slice(0, maxChars - 1) + "…";
}

function extractField(markdown, field) {
  const re = new RegExp(`^- \\*\\*${field}:\\*\\*\\s*(.*)$`, "mi");
  const m = markdown.match(re);
  return m ? m[1].trim() : "";
}

function execJson(command, args, timeoutMs = 4000) {
  return new Promise((resolve) => {
    execFile(command, args, { cwd: WORKSPACE, timeout: timeoutMs, encoding: "utf8", windowsHide: true }, (error, stdout) => {
      if (error && !stdout) return resolve(null);
      const text = (stdout || "").trim();
      if (!text) return resolve(null);
      const lines = text.split(/\r?\n/).filter(Boolean).reverse();
      for (const line of lines) {
        try {
          return resolve(JSON.parse(line));
        } catch {}
      }
      try {
        resolve(JSON.parse(text));
      } catch {
        resolve(null);
      }
    });
  });
}

async function getCronSummary() {
  const data = await execJson("openclaw", ["cron", "list", "--json", "--timeout", "4000"]);
  const jobs = Array.isArray(data?.jobs) ? data.jobs : Array.isArray(data) ? data : [];
  if (!jobs.length) return "No active cron jobs found.";
  return jobs.slice(0, 8).map((job, i) => {
    const name = job.name || job.id || `job-${i + 1}`;
    const schedule = job.schedule?.expr || job.schedule?.kind || "schedule unknown";
    const enabled = job.enabled === false ? "disabled" : "enabled";
    return `${i + 1}. ${name} (${enabled}) - ${schedule}`;
  }).join("\n");
}

async function getTaskSummary() {
  const data = await execJson("openclaw", ["tasks", "list", "--json"]);
  const tasks = Array.isArray(data?.tasks) ? data.tasks : Array.isArray(data) ? data : [];
  if (!tasks.length) return "No tracked background tasks found.";
  return tasks.slice(0, 8).map((task, i) => {
    const label = task.label || task.name || task.taskId || `task-${i + 1}`;
    const status = task.status || "unknown";
    const runtime = task.runtime || task.kind || "runtime unknown";
    return `${i + 1}. ${label} - ${status} (${runtime})`;
  }).join("\n");
}

function getBasicProfile() {
  const identityMd = readTextSafe(path.join(WORKSPACE, "IDENTITY.md"));
  const userMd = readTextSafe(path.join(WORKSPACE, "USER.md"));

  const identity = extractField(identityMd, "Name") || "jhon";
  const user = extractField(userMd, "What to call them") || extractField(userMd, "Name") || "the user";
  const timezone = extractField(userMd, "Timezone") || "unknown";
  const notes = compact(extractField(userMd, "Notes") || "", 280);

  return { identity, user, timezone, notes };
}

async function buildPhoneContext(message = "") {
  const profile = getBasicProfile();
  const lower = String(message || "").toLowerCase();
  const wantsCron = /cron|reminder|schedule|scheduled|job/.test(lower);
  const wantsTasks = /task|tasks|background|running|pending/.test(lower);
  const wantsMemory = /remember|preference|prefer|who am i|who is sam/.test(lower);

  const memoryMd = wantsMemory ? readTextSafe(path.join(WORKSPACE, "MEMORY.md")) : "";
  const memorySnippet = compact(memoryMd, 700);

  const blocks = [
    `User name: ${profile.user}`,
    `Timezone: ${profile.timezone}`,
    profile.notes ? `User notes: ${profile.notes}` : "",
  ].filter(Boolean);

  const promises = [];
  if (wantsCron) promises.push(getCronSummary().then((v) => ({ key: "cron", value: v })));
  if (wantsTasks) promises.push(getTaskSummary().then((v) => ({ key: "tasks", value: v })));
  const resolved = await Promise.all(promises);
  for (const item of resolved) {
    if (item.key === "cron") blocks.push(`Cron jobs:\n${item.value}`);
    if (item.key === "tasks") blocks.push(`Tasks:\n${item.value}`);
  }

  if (memorySnippet) blocks.push(`Long-term memory excerpt:\n${memorySnippet}`);

  return {
    identity: profile.identity,
    user: profile.user,
    timezone: profile.timezone,
    notes: profile.notes,
    contextText: blocks.join("\n\n"),
  };
}

module.exports = { buildPhoneContext, getBasicProfile, getCronSummary, getTaskSummary };

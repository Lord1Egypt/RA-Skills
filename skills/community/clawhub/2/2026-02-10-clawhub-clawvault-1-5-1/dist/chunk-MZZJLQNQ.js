// src/commands/checkpoint.ts
import * as fs from "fs";
import * as path from "path";
import { execFileSync } from "child_process";
var CLAWVAULT_DIR = ".clawvault";
var CHECKPOINT_FILE = "last-checkpoint.json";
var SESSION_STATE_FILE = "session-state.json";
var DIRTY_DEATH_FLAG = "dirty-death.flag";
var pendingCheckpoint = null;
var pendingData = null;
function ensureClawvaultDir(vaultPath) {
  const dir = path.join(vaultPath, CLAWVAULT_DIR);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  return dir;
}
function writeCheckpointToDisk(dir, data) {
  const checkpointPath = path.join(dir, CHECKPOINT_FILE);
  fs.writeFileSync(checkpointPath, JSON.stringify(data, null, 2));
  const flagPath = path.join(dir, DIRTY_DEATH_FLAG);
  fs.writeFileSync(flagPath, data.timestamp);
}
function parseTokenEstimate(raw) {
  if (!raw) return void 0;
  const parsed = Number(raw);
  return Number.isFinite(parsed) ? parsed : void 0;
}
function loadSessionState(dir) {
  const sessionStatePath = path.join(dir, SESSION_STATE_FILE);
  if (!fs.existsSync(sessionStatePath)) return null;
  try {
    return JSON.parse(fs.readFileSync(sessionStatePath, "utf-8"));
  } catch {
    return null;
  }
}
function getEnvSessionState() {
  return {
    sessionKey: process.env.OPENCLAW_SESSION_KEY,
    model: process.env.OPENCLAW_MODEL,
    tokenEstimate: parseTokenEstimate(
      process.env.OPENCLAW_TOKEN_ESTIMATE || process.env.OPENCLAW_CONTEXT_TOKENS
    )
  };
}
function triggerUrgentWake(data) {
  const summary = [
    data.workingOn ? `Working on: ${data.workingOn}` : null,
    data.focus ? `Focus: ${data.focus}` : null,
    data.blocked ? `Blocked: ${data.blocked}` : null
  ].filter(Boolean).join(" | ");
  const text = summary ? `Urgent checkpoint saved. ${summary}` : "Urgent checkpoint saved.";
  try {
    execFileSync("openclaw", ["gateway", "wake", "--text", text, "--mode", "now"], {
      stdio: "inherit"
    });
  } catch (err) {
    if (err?.code === "ENOENT") {
      throw new Error("Urgent wake failed: openclaw CLI not found.");
    }
    throw new Error(`Urgent wake failed: ${err?.message || "unknown error"}`);
  }
}
async function flush() {
  if (pendingCheckpoint) {
    clearTimeout(pendingCheckpoint);
    pendingCheckpoint = null;
  }
  if (!pendingData) return null;
  const { dir, data } = pendingData;
  pendingData = null;
  writeCheckpointToDisk(dir, data);
  return data;
}
async function checkpoint(options) {
  const dir = ensureClawvaultDir(options.vaultPath);
  const data = {
    timestamp: (/* @__PURE__ */ new Date()).toISOString(),
    workingOn: options.workingOn || null,
    focus: options.focus || null,
    blocked: options.blocked || null,
    urgent: options.urgent || false
  };
  const sessionState = loadSessionState(dir);
  const envState = getEnvSessionState();
  data.sessionId = sessionState?.sessionId;
  data.sessionKey = envState.sessionKey || sessionState?.sessionKey || sessionState?.sessionId;
  data.model = envState.model || sessionState?.model;
  data.tokenEstimate = envState.tokenEstimate ?? sessionState?.tokenEstimate;
  data.sessionStartedAt = sessionState?.startedAt;
  if (options.urgent) {
    if (pendingCheckpoint) {
      clearTimeout(pendingCheckpoint);
      pendingCheckpoint = null;
    }
    pendingData = null;
    writeCheckpointToDisk(dir, data);
    triggerUrgentWake(data);
  } else {
    pendingData = { dir, data };
    if (pendingCheckpoint) clearTimeout(pendingCheckpoint);
    pendingCheckpoint = setTimeout(() => {
      void flush();
    }, 1e3);
  }
  return data;
}
async function clearDirtyFlag(vaultPath) {
  const flagPath = path.join(vaultPath, CLAWVAULT_DIR, DIRTY_DEATH_FLAG);
  if (fs.existsSync(flagPath)) {
    fs.unlinkSync(flagPath);
  }
}
async function cleanExit(vaultPath) {
  await clearDirtyFlag(vaultPath);
}
async function checkDirtyDeath(vaultPath) {
  const dir = path.join(vaultPath, CLAWVAULT_DIR);
  const flagPath = path.join(dir, DIRTY_DEATH_FLAG);
  const checkpointPath = path.join(dir, CHECKPOINT_FILE);
  if (!fs.existsSync(flagPath)) {
    return { died: false, checkpoint: null, deathTime: null };
  }
  const deathTime = fs.readFileSync(flagPath, "utf-8").trim();
  let checkpoint2 = null;
  if (fs.existsSync(checkpointPath)) {
    try {
      checkpoint2 = JSON.parse(fs.readFileSync(checkpointPath, "utf-8"));
    } catch {
    }
  }
  return { died: true, checkpoint: checkpoint2, deathTime };
}
async function setSessionState(vaultPath, session) {
  const dir = ensureClawvaultDir(vaultPath);
  const sessionStatePath = path.join(dir, SESSION_STATE_FILE);
  const state = typeof session === "string" ? { sessionId: session } : { ...session };
  if (!state.startedAt) {
    state.startedAt = (/* @__PURE__ */ new Date()).toISOString();
  }
  fs.writeFileSync(sessionStatePath, JSON.stringify(state, null, 2));
}

export {
  flush,
  checkpoint,
  clearDirtyFlag,
  cleanExit,
  checkDirtyDeath,
  setSessionState
};

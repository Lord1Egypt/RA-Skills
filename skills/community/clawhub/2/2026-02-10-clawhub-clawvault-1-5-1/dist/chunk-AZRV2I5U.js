// src/lib/session-utils.ts
import * as fs from "fs";
import * as path from "path";
import * as os from "os";
function getOpenClawAgentsDir() {
  return path.join(os.homedir(), ".openclaw", "agents");
}
function getSessionsDir(agentId) {
  return path.join(getOpenClawAgentsDir(), agentId, "sessions");
}
function getSessionsJsonPath(agentId) {
  return path.join(getSessionsDir(agentId), "sessions.json");
}
function getSessionFilePath(agentId, sessionId) {
  return path.join(getSessionsDir(agentId), `${sessionId}.jsonl`);
}
function listAgents() {
  const agentsDir = getOpenClawAgentsDir();
  if (!fs.existsSync(agentsDir)) {
    return [];
  }
  return fs.readdirSync(agentsDir).filter((name) => {
    const sessionsDir = getSessionsDir(name);
    return fs.existsSync(sessionsDir) && fs.statSync(sessionsDir).isDirectory();
  });
}
function loadSessionsStore(agentId) {
  const sessionsJsonPath = getSessionsJsonPath(agentId);
  if (!fs.existsSync(sessionsJsonPath)) {
    return null;
  }
  try {
    const content = fs.readFileSync(sessionsJsonPath, "utf-8");
    return JSON.parse(content);
  } catch {
    return null;
  }
}
function findMainSession(agentId) {
  const store = loadSessionsStore(agentId);
  if (!store) return null;
  const mainKey = `agent:${agentId}:main`;
  const entry = store[mainKey];
  if (entry?.sessionId) {
    const filePath = getSessionFilePath(agentId, entry.sessionId);
    if (fs.existsSync(filePath)) {
      return {
        sessionId: entry.sessionId,
        sessionKey: mainKey,
        agentId,
        filePath,
        updatedAt: entry.updatedAt
      };
    }
  }
  return null;
}
function findSessionById(agentId, sessionId) {
  const filePath = getSessionFilePath(agentId, sessionId);
  if (!fs.existsSync(filePath)) {
    return null;
  }
  const store = loadSessionsStore(agentId);
  let sessionKey;
  let updatedAt;
  if (store) {
    for (const [key, entry] of Object.entries(store)) {
      if (entry.sessionId === sessionId) {
        sessionKey = key;
        updatedAt = entry.updatedAt;
        break;
      }
    }
  }
  return {
    sessionId,
    sessionKey: sessionKey || `agent:${agentId}:unknown`,
    agentId,
    filePath,
    updatedAt
  };
}
function listSessions(agentId) {
  const sessionsDir = getSessionsDir(agentId);
  if (!fs.existsSync(sessionsDir)) {
    return [];
  }
  const store = loadSessionsStore(agentId);
  const sessions = [];
  const files = fs.readdirSync(sessionsDir).filter((f) => f.endsWith(".jsonl") && !f.includes(".backup") && !f.includes(".deleted") && !f.includes(".corrupted"));
  for (const file of files) {
    const sessionId = file.replace(".jsonl", "");
    const filePath = path.join(sessionsDir, file);
    let sessionKey = `agent:${agentId}:unknown`;
    let updatedAt;
    if (store) {
      for (const [key, entry] of Object.entries(store)) {
        if (entry.sessionId === sessionId) {
          sessionKey = key;
          updatedAt = entry.updatedAt;
          break;
        }
      }
    }
    sessions.push({
      sessionId,
      sessionKey,
      agentId,
      filePath,
      updatedAt
    });
  }
  return sessions.sort((a, b) => (b.updatedAt || 0) - (a.updatedAt || 0));
}
function backupSession(filePath) {
  const timestamp = (/* @__PURE__ */ new Date()).toISOString().replace(/[:.]/g, "").replace("T", "-").slice(0, 15);
  const backupPath = `${filePath}.backup-${timestamp}`;
  fs.copyFileSync(filePath, backupPath);
  return backupPath;
}

export {
  getOpenClawAgentsDir,
  getSessionsDir,
  getSessionsJsonPath,
  getSessionFilePath,
  listAgents,
  loadSessionsStore,
  findMainSession,
  findSessionById,
  listSessions,
  backupSession
};

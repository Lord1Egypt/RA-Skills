import {
  analyzeSession,
  repairSession
} from "../chunk-L53L5FCL.js";
import {
  findMainSession,
  findSessionById,
  listAgents
} from "../chunk-AZRV2I5U.js";

// src/commands/repair-session.ts
import * as fs from "fs";
function resolveSession(options) {
  const { sessionId, agentId } = options;
  if (sessionId && agentId) {
    return findSessionById(agentId, sessionId);
  }
  if (sessionId) {
    const agents = listAgents();
    for (const agent of agents) {
      const session = findSessionById(agent, sessionId);
      if (session) return session;
    }
    return null;
  }
  if (agentId) {
    return findMainSession(agentId);
  }
  const defaultAgent = process.env.OPENCLAW_AGENT_ID || "clawdious";
  return findMainSession(defaultAgent);
}
function formatRepairResult(result, options = {}) {
  const { dryRun = false } = options;
  const lines = [];
  lines.push(`Analyzing session: ${result.sessionId}`);
  lines.push("");
  if (result.corruptedEntries.length === 0) {
    lines.push("\u2705 No corruption detected. Session is clean.");
    return lines.join("\n");
  }
  if (dryRun) {
    lines.push(`Found ${result.corruptedEntries.length} corrupted entries:`);
  } else {
    lines.push(`Found and fixed ${result.corruptedEntries.length} corrupted entries:`);
  }
  for (const entry of result.corruptedEntries) {
    const prefix = entry.type === "aborted_tool_use" ? "Aborted tool_use" : "Orphaned tool_result";
    lines.push(`  - Line ${entry.lineNumber}: ${prefix} (id: ${entry.toolUseId})`);
  }
  if (result.parentRelinks.length > 0) {
    lines.push("");
    if (dryRun) {
      lines.push(`Would relink ${result.parentRelinks.length} parent reference(s):`);
    } else {
      lines.push(`Relinked ${result.parentRelinks.length} parent reference(s):`);
    }
    for (const relink of result.parentRelinks.slice(0, 5)) {
      lines.push(`  - Line ${relink.lineNumber}: parentId ${relink.oldParentId.slice(0, 8)}\u2026 \u2192 ${relink.newParentId === "null" ? "null" : relink.newParentId.slice(0, 8)}\u2026`);
    }
    if (result.parentRelinks.length > 5) {
      lines.push(`  ... and ${result.parentRelinks.length - 5} more`);
    }
  }
  lines.push("");
  if (dryRun) {
    lines.push(`Would remove ${result.removedCount} entries, relink ${result.relinkedCount} parent references.`);
  } else {
    lines.push(`\u2705 Session repaired: removed ${result.removedCount} entries, relinked ${result.relinkedCount} parent references`);
    if (result.backupPath) {
      const backupName = result.backupPath.split("/").pop();
      lines.push(`Backup saved: ${backupName}`);
    }
  }
  return lines.join("\n");
}
async function repairSessionCommand(options) {
  const { backup = true, dryRun = false } = options;
  const session = resolveSession(options);
  if (!session) {
    throw new Error(
      options.sessionId ? `Session not found: ${options.sessionId}` : options.agentId ? `No main session found for agent: ${options.agentId}` : "No session found. Specify --session or --agent."
    );
  }
  if (!fs.existsSync(session.filePath)) {
    throw new Error(`Session file not found: ${session.filePath}`);
  }
  if (dryRun) {
    return analyzeSession(session.filePath);
  }
  return repairSession(session.filePath, { backup, dryRun: false });
}
function listAgentSessions(agentId) {
  const agents = agentId ? [agentId] : listAgents();
  const lines = [];
  if (agents.length === 0) {
    return "No agents found in ~/.openclaw/agents/";
  }
  for (const agent of agents) {
    const mainSession = findMainSession(agent);
    if (mainSession) {
      lines.push(`${agent}:`);
      lines.push(`  Main session: ${mainSession.sessionId}`);
      lines.push(`  File: ${mainSession.filePath}`);
      if (mainSession.updatedAt) {
        const date = new Date(mainSession.updatedAt);
        lines.push(`  Updated: ${date.toISOString()}`);
      }
      lines.push("");
    }
  }
  if (lines.length === 0) {
    return agentId ? `No sessions found for agent: ${agentId}` : "No sessions found.";
  }
  return lines.join("\n");
}
export {
  formatRepairResult,
  listAgentSessions,
  repairSessionCommand,
  resolveSession
};

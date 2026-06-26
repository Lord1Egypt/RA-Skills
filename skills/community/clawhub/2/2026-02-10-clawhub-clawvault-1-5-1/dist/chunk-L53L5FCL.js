// src/lib/session-repair.ts
import * as fs from "fs";
function parseTranscript(filePath) {
  const content = fs.readFileSync(filePath, "utf-8");
  const lines = content.split("\n").filter((line) => line.trim());
  const entries = [];
  for (let i = 0; i < lines.length; i++) {
    const raw = lines[i];
    try {
      const entry = JSON.parse(raw);
      entries.push({ line: i + 1, entry, raw });
    } catch {
      console.warn(`Warning: Could not parse line ${i + 1}`);
    }
  }
  return entries;
}
function extractToolUses(entries) {
  const toolUses = /* @__PURE__ */ new Map();
  for (const { line, entry } of entries) {
    if (entry.type !== "message") continue;
    if (entry.message?.role !== "assistant") continue;
    const isAborted = entry.message.stopReason === "aborted";
    const content = entry.message.content || [];
    for (const block of content) {
      if (block.type === "toolCall" || block.type === "tool_use" || block.type === "functionCall") {
        if (block.id) {
          const isPartial = !!block.partialJson;
          toolUses.set(block.id, {
            id: block.id,
            lineNumber: line,
            entryId: entry.id,
            isAborted: isAborted || isPartial,
            isPartial,
            name: block.name
          });
        }
      }
    }
  }
  return toolUses;
}
function findCorruptedEntries(entries, toolUses) {
  const corrupted = [];
  const entriesToRemove = /* @__PURE__ */ new Set();
  for (const [toolId, info] of toolUses) {
    if (info.isAborted) {
      corrupted.push({
        lineNumber: info.lineNumber,
        entryId: info.entryId,
        type: "aborted_tool_use",
        toolUseId: toolId,
        description: `Aborted tool_use${info.name ? ` (${info.name})` : ""} with id: ${toolId}`
      });
      entriesToRemove.add(info.entryId);
    }
  }
  for (const { line, entry } of entries) {
    if (entry.type !== "message") continue;
    if (entry.message?.role !== "toolResult") continue;
    const content = entry.message.content || [];
    let toolCallId;
    const msg = entry.message;
    toolCallId = msg.toolCallId || msg.toolUseId;
    if (!toolCallId) {
      for (const block of content) {
        if (block.toolCallId || block.toolUseId) {
          toolCallId = block.toolCallId || block.toolUseId;
          break;
        }
      }
    }
    if (!toolCallId) continue;
    const toolUse = toolUses.get(toolCallId);
    if (!toolUse || toolUse.isAborted) {
      corrupted.push({
        lineNumber: line,
        entryId: entry.id,
        type: "orphaned_tool_result",
        toolUseId: toolCallId,
        description: toolUse ? `Orphaned tool_result references aborted tool_use: ${toolCallId}` : `Orphaned tool_result references non-existent tool_use: ${toolCallId}`
      });
      entriesToRemove.add(entry.id);
    }
  }
  return { corrupted, entriesToRemove };
}
function computeParentRelinks(entries, entriesToRemove) {
  const relinks = [];
  const entryParents = /* @__PURE__ */ new Map();
  for (const { entry } of entries) {
    entryParents.set(entry.id, entry.parentId);
  }
  for (const { line, entry } of entries) {
    if (entriesToRemove.has(entry.id)) continue;
    if (!entry.parentId) continue;
    if (!entriesToRemove.has(entry.parentId)) continue;
    let newParentId = entry.parentId;
    while (newParentId && entriesToRemove.has(newParentId)) {
      newParentId = entryParents.get(newParentId) || null;
    }
    if (newParentId !== entry.parentId) {
      relinks.push({
        lineNumber: line,
        entryId: entry.id,
        oldParentId: entry.parentId,
        newParentId: newParentId || "null"
      });
    }
  }
  return relinks;
}
function analyzeSession(filePath) {
  const entries = parseTranscript(filePath);
  const sessionEntry = entries.find((e) => e.entry.type === "session");
  const sessionId = sessionEntry?.entry.id || "unknown";
  const toolUses = extractToolUses(entries);
  const { corrupted, entriesToRemove } = findCorruptedEntries(entries, toolUses);
  const parentRelinks = computeParentRelinks(entries, entriesToRemove);
  return {
    sessionId,
    totalLines: entries.length,
    corruptedEntries: corrupted,
    parentRelinks,
    removedCount: entriesToRemove.size,
    relinkedCount: parentRelinks.length,
    repaired: false
  };
}
function repairSession(filePath, options = {}) {
  const { backup = true, dryRun = false } = options;
  const entries = parseTranscript(filePath);
  const sessionEntry = entries.find((e) => e.entry.type === "session");
  const sessionId = sessionEntry?.entry.id || "unknown";
  const toolUses = extractToolUses(entries);
  const { corrupted, entriesToRemove } = findCorruptedEntries(entries, toolUses);
  const parentRelinks = computeParentRelinks(entries, entriesToRemove);
  if (corrupted.length === 0) {
    return {
      sessionId,
      totalLines: entries.length,
      corruptedEntries: [],
      parentRelinks: [],
      removedCount: 0,
      relinkedCount: 0,
      repaired: false
    };
  }
  if (dryRun) {
    return {
      sessionId,
      totalLines: entries.length,
      corruptedEntries: corrupted,
      parentRelinks,
      removedCount: entriesToRemove.size,
      relinkedCount: parentRelinks.length,
      repaired: false
    };
  }
  let backupPath;
  if (backup) {
    const timestamp = (/* @__PURE__ */ new Date()).toISOString().replace(/[:.]/g, "").replace("T", "-").slice(0, 15);
    backupPath = `${filePath}.backup-${timestamp}`;
    fs.copyFileSync(filePath, backupPath);
  }
  const relinkMap = /* @__PURE__ */ new Map();
  for (const relink of parentRelinks) {
    relinkMap.set(relink.entryId, relink.newParentId === "null" ? null : relink.newParentId);
  }
  const repairedLines = [];
  for (const { entry, raw } of entries) {
    if (entriesToRemove.has(entry.id)) continue;
    if (relinkMap.has(entry.id)) {
      const newEntry = { ...entry, parentId: relinkMap.get(entry.id) };
      repairedLines.push(JSON.stringify(newEntry));
    } else {
      repairedLines.push(raw);
    }
  }
  fs.writeFileSync(filePath, repairedLines.join("\n") + "\n");
  return {
    sessionId,
    totalLines: entries.length,
    corruptedEntries: corrupted,
    parentRelinks,
    removedCount: entriesToRemove.size,
    relinkedCount: parentRelinks.length,
    backupPath,
    repaired: true
  };
}

export {
  parseTranscript,
  extractToolUses,
  findCorruptedEntries,
  computeParentRelinks,
  analyzeSession,
  repairSession
};

import { existsSync, readFileSync, readdirSync } from "fs";
import { resolve } from "path";
import { homedir } from "os";
import { DATA_DIR, loadJson, saveJson } from "./persistence.ts";
import { addMemory } from "./memory.ts";
import { spawnCLI } from "./cli.ts";
const IMPORT_MARKER = resolve(DATA_DIR, "import_done.json");
const AGENTS_DIR = resolve(homedir(), ".openclaw/agents");
function needsImport() {
  const state = loadJson(IMPORT_MARKER, { done: false, importedAt: 0, sessionsScanned: 0, memoriesExtracted: 0 });
  return !state.done;
}
function autoImportHistory() {
  if (!needsImport()) return;
  if (!existsSync(AGENTS_DIR)) return;
  console.log(`[cc-soul][import] scanning historical sessions...`);
  const sessionFiles = [];
  try {
    const agents = readdirSync(AGENTS_DIR);
    for (const agent of agents) {
      const sessionsDir = resolve(AGENTS_DIR, agent, "sessions");
      if (!existsSync(sessionsDir)) continue;
      const files = readdirSync(sessionsDir).filter((f) => f.endsWith(".jsonl"));
      for (const f of files) {
        sessionFiles.push(resolve(sessionsDir, f));
      }
    }
  } catch (e) {
    console.error(`[cc-soul][import] scan error: ${e.message}`);
    return;
  }
  if (sessionFiles.length === 0) {
    console.log(`[cc-soul][import] no session files found`);
    markDone(0, 0);
    return;
  }
  console.log(`[cc-soul][import] found ${sessionFiles.length} session files`);
  let totalMessages = 0;
  const conversations = [];
  for (const file of sessionFiles) {
    try {
      const raw = readFileSync(file, "utf-8");
      const lines = raw.split("\n").filter((l) => l.trim());
      const turns = [];
      for (const line of lines) {
        try {
          const entry = JSON.parse(line);
          if (entry.type !== "message") continue;
          const msg = entry.message;
          if (!msg || !msg.role) continue;
          let text = "";
          if (typeof msg.content === "string") {
            text = msg.content;
          } else if (Array.isArray(msg.content)) {
            text = msg.content.filter((c) => typeof c === "object" && c.text).map((c) => c.text).join(" ");
          }
          if (!text || text.length < 5) continue;
          text = text.replace(/^Conversation info \(untrusted metadata\):[\s\S]*?```\n/m, "").trim();
          if (!text || text.length < 10) continue;
          turns.push(`[${msg.role}] ${text.slice(0, 300)}`);
          totalMessages++;
        } catch {
        }
      }
      if (turns.length >= 2) {
        conversations.push(turns.slice(-20).join("\n"));
      }
    } catch {
    }
  }
  if (conversations.length === 0) {
    console.log(`[cc-soul][import] no valid conversations found`);
    markDone(sessionFiles.length, 0);
    return;
  }
  console.log(`[cc-soul][import] extracted ${totalMessages} messages from ${conversations.length} sessions, sending to CLI for analysis...`);
  let extracted = 0;
  const batches = [];
  for (let i = 0; i < conversations.length; i += 3) {
    batches.push(conversations.slice(i, i + 3));
  }
  let batchIndex = 0;
  function processBatch() {
    if (batchIndex >= batches.length) {
      markDone(sessionFiles.length, extracted);
      console.log(`[cc-soul][import] complete: ${extracted} memories from ${sessionFiles.length} sessions`);
      return;
    }
    const batch = batches[batchIndex];
    const combined = batch.join("\n\n---\n\n").slice(0, 3e3);
    spawnCLI(
      `Extract important facts, preferences, and key information from these historical conversations. Each line should be one memory, format: [type] content
Types: fact, preference, event, opinion
Only extract genuinely useful long-term information. Skip greetings and small talk.
If nothing worth remembering, reply "none".

Conversations:
${combined}`,
      (output) => {
        if (output && !output.toLowerCase().includes("none")) {
          const lines = output.split("\n").filter((l) => l.trim().length > 10);
          for (const line of lines.slice(0, 10)) {
            const match = line.match(/\[(\w+)\]\s*(.+)/);
            if (match) {
              const scope = match[1] === "preference" ? "preference" : "fact";
              addMemory(`[historical] ${match[2].trim()}`, scope, void 0, "global");
              extracted++;
            }
          }
        }
        batchIndex++;
        setTimeout(processBatch, 3e3);
      },
      45e3
    );
  }
  setTimeout(processBatch, 5e3);
}
function markDone(sessions, memories) {
  saveJson(IMPORT_MARKER, {
    done: true,
    importedAt: Date.now(),
    sessionsScanned: sessions,
    memoriesExtracted: memories
  });
}
const historyImportModule = {
  id: "history-import",
  name: "\u5386\u53F2\u5BFC\u5165",
  priority: 50
};
export {
  autoImportHistory,
  historyImportModule,
  needsImport
};

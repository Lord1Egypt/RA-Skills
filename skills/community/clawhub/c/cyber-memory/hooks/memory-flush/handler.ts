import path from "node:path";
import fs from "node:fs/promises";
import os from "node:os";

// --- Config ---

const DEFAULT_LLM_BASE = "http://localhost:11434/v1/chat/completions";
const DEFAULT_EXTRACTION_MODEL = "qwen2.5:7b";
const MAX_TRANSCRIPT_CHARS = 8000;

// --- Logging ---

function log(msg: string, meta?: Record<string, unknown>) {
  const ts = new Date().toISOString();
  const metaStr = meta ? ` ${JSON.stringify(meta)}` : "";
  console.log(`[memory-flush ${ts}] ${msg}${metaStr}`);
}

// --- Transcript reading ---

async function readRecentMessages(sessionFile: string, count: number): Promise<{ raw: string; messages: string[] }> {
  try {
    const content = await fs.readFile(sessionFile, "utf-8");
    const lines = content.trim().split("\n");
    const messages: string[] = [];

    for (const line of lines) {
      try {
        const entry = JSON.parse(line);
        if (entry.type === "message" && entry.message) {
          const msg = entry.message;
          const role = msg.role;
          if (role === "user" || role === "assistant") {
            const text = Array.isArray(msg.content)
              ? msg.content.find((c: { type: string }) => c.type === "text")?.text
              : msg.content;
            if (text && typeof text === "string" && !text.startsWith("/")) {
              const truncated = text.slice(0, 500);
              messages.push(`${role}: ${truncated}`);
            }
          }
        }
      } catch {
        // skip non-JSON lines
      }
    }

    const recent = messages.slice(-count);
    return { raw: recent.join("\n"), messages: recent };
  } catch (err) {
    log("Failed to read session file", { file: sessionFile, error: String(err) });
    return { raw: "", messages: [] };
  }
}

async function findSessionFile(sessionsDir: string, sessionId: string): Promise<string | null> {
  try {
    const files = await fs.readdir(sessionsDir);
    const exact = `${sessionId}.jsonl`;
    if (files.includes(exact)) return path.join(sessionsDir, exact);

    const variants = files
      .filter((f) => f.startsWith(sessionId) && f.endsWith(".jsonl") && !f.includes(".reset."))
      .sort()
      .reverse();
    if (variants.length > 0) return path.join(sessionsDir, variants[0]);

    const recent = files
      .filter((f) => f.endsWith(".jsonl") && !f.includes(".reset."))
      .sort()
      .reverse();
    if (recent.length > 0) return path.join(sessionsDir, recent[0]);
  } catch {
    // directory not found
  }
  return null;
}

// --- Fact extraction via LLM ---

async function extractFacts(transcript: string, apiKey: string, model?: string, baseUrl?: string): Promise<string> {
  if (!transcript.trim() || transcript.length < 50) {
    return "";
  }

  const truncated = transcript.length > MAX_TRANSCRIPT_CHARS
    ? transcript.slice(-MAX_TRANSCRIPT_CHARS)
    : transcript;

  const prompt = `你是一个事实提取器。从以下对话中提取值得长期记忆的信息。

只提取以下类型的事实：
- 用户偏好（喜欢什么、习惯什么、选择什么）
- 重要决定（选了什么方案、用什么工具、定什么规则）
- 约定和规则（以后怎么做、什么不能做）
- 重要信息（账号、项目名、联系人、时间安排）

输出格式（每条一行，前缀标注类型）：
[PREF] 用户偏好内容
[DECIDE] 决策内容
[RULE] 规则/约定内容
[INFO] 重要信息内容

如果没有值得记忆的事实，输出 "NONE"。

对话内容：
${truncated}`;

  const endpoint = baseUrl || DEFAULT_LLM_BASE;
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };
  // Ollama uses "Bearer ollama" or no auth; OpenAI uses "Bearer <key>"
  if (apiKey && apiKey !== "ollama") {
    headers["Authorization"] = `Bearer ${apiKey}`;
  }

  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers,
      body: JSON.stringify({
        model: model || DEFAULT_EXTRACTION_MODEL,
        messages: [{ role: "user", content: prompt }],
        max_tokens: 500,
        temperature: 0.1,
      }),
    });

    if (!response.ok) {
      log("LLM extraction failed", { status: response.status, statusText: response.statusText });
      return "";
    }

    const data = await response.json() as {
      choices?: Array<{ message?: { content?: string } }>;
    };
    const result = data.choices?.[0]?.message?.content?.trim() || "";

    if (result === "NONE" || result.length < 10) {
      return "";
    }

    return result;
  } catch (err) {
    log("LLM extraction error", { error: String(err) });
    return "";
  }
}

// --- Helpers ---

function resolveWorkspaceDir(context: Record<string, unknown>): string {
  const wsDir = context.workspaceDir as string | undefined;
  if (wsDir && wsDir.trim().length > 0) return wsDir;
  return path.join(os.homedir(), ".openclaw", "workspace");
}

function resolveSessionsDir(workspaceDir: string): string {
  const agentDir = path.dirname(workspaceDir);
  return path.join(agentDir, "sessions");
}

function resolveApiKey(cfg: Record<string, unknown> | undefined): string {
  const providers = (cfg?.models as Record<string, unknown>)?.providers as Record<string, Record<string, string>> | undefined;
  return providers?.openai?.apiKey
    || process.env.OPENAI_API_KEY
    || "ollama";
}

function resolveBaseUrl(cfg: Record<string, unknown> | undefined): string {
  const hookConfig = (cfg?.hooks as Record<string, unknown>)?.internal as Record<string, unknown> | undefined;
  const entries = hookConfig?.entries as Record<string, Record<string, unknown>> | undefined;
  const flushConfig = entries?.["memory-flush"] as Record<string, unknown> | undefined;
  return (flushConfig?.baseUrl as string) || DEFAULT_LLM_BASE;
}

function resolveExtractionModel(cfg: Record<string, unknown> | undefined): string {
  const hookConfig = (cfg?.hooks as Record<string, unknown>)?.internal as Record<string, unknown> | undefined;
  const entries = hookConfig?.entries as Record<string, Record<string, unknown>> | undefined;
  const flushConfig = entries?.["memory-flush"] as Record<string, unknown> | undefined;
  return (flushConfig?.extractionModel as string) || DEFAULT_EXTRACTION_MODEL;
}

async function writeFileSafe(dir: string, filename: string, content: string) {
  await fs.mkdir(dir, { recursive: true });
  const filePath = path.join(dir, filename);
  await fs.writeFile(filePath, content, "utf-8");
  return filePath;
}

// --- Handlers ---

async function onCompactBefore(event: {
  sessionKey: string;
  timestamp: Date;
  context: Record<string, unknown>;
  messages: string[];
}) {
  const ctx = event.context || {};
  const sessionId = (ctx.sessionId as string) || "unknown";
  const messageCount = (ctx.messageCount as number) || 0;
  const tokenCount = (ctx.tokenCount as number) || 0;

  log("Compaction starting — extracting facts", { sessionId, messageCount, tokenCount });

  const workspaceDir = resolveWorkspaceDir(ctx);
  const memoryDir = path.join(workspaceDir, "memory");
  const sessionsDir = resolveSessionsDir(workspaceDir);

  const sessionFile = await findSessionFile(sessionsDir, sessionId);
  let transcript = "";
  let rawMessages: string[] = [];

  if (sessionFile) {
    log("Reading session file", { file: sessionFile.replace(os.homedir(), "~") });
    const result = await readRecentMessages(sessionFile, 30);
    transcript = result.raw;
    rawMessages = result.messages;
  } else {
    log("Session file not found", { sessionId, sessionsDir });
  }

  const cfg = (ctx.cfg || {}) as Record<string, unknown>;
  const apiKey = resolveApiKey(cfg);
  const baseUrl = resolveBaseUrl(cfg);
  const extractionModel = resolveExtractionModel(cfg);
  let extractedFacts = "";

  if (transcript) {
    log("Calling LLM for fact extraction", { model: extractionModel, baseUrl, transcriptLen: transcript.length });
    extractedFacts = await extractFacts(transcript, apiKey, extractionModel, baseUrl);
    log("Fact extraction done", { factsFound: extractedFacts.length > 0, length: extractedFacts.length });
  } else {
    log("Skipping LLM extraction", { hasTranscript: !!transcript });
  }

  const now = event.timestamp;
  const dateStr = now.toISOString().split("T")[0];
  const timeStr = now.toISOString().split("T")[1].split(".")[0];
  const timeClean = timeStr.replace(/:/g, "");

  if (extractedFacts) {
    const factLines = extractedFacts.split("\n").filter(l => l.trim());
    const factContent = [
      `# Extracted Facts — ${dateStr} ${timeStr}`,
      "",
      `- **Session**: ${event.sessionKey}`,
      `- **Session ID**: ${sessionId}`,
      "",
      "## Facts",
      "",
      ...factLines,
      "",
      "---",
      `_Auto-extracted by memory-flush hook at compaction_`,
      "",
    ].join("\n");

    const factFile = await writeFileSafe(memoryDir, `${dateStr}-facts-${timeClean}.md`, factContent);
    log("Facts saved", { file: factFile.replace(os.homedir(), "~"), factCount: factLines.length });
  }

  if (rawMessages.length > 0) {
    const snapshotContent = [
      `# Pre-Compaction Snapshot — ${dateStr} ${timeStr}`,
      "",
      `- **Session**: ${event.sessionKey}`,
      `- **Messages**: ${messageCount} | **Tokens**: ${tokenCount}`,
      "",
      "## Recent Conversation",
      "",
      ...rawMessages.slice(-15),
      "",
      "---",
      `_Auto-saved by memory-flush hook_`,
      "",
    ].join("\n");

    await writeFileSafe(memoryDir, `${dateStr}-compact-${timeClean}.md`, snapshotContent);
  }
}

async function onCommandNew(event: {
  action: string;
  sessionKey: string;
  timestamp: Date;
  context: Record<string, unknown>;
  messages: string[];
}) {
  if (event.action !== "new" && event.action !== "reset") return;

  const ctx = event.context || {};
  const workspaceDir = resolveWorkspaceDir(ctx);
  const memoryDir = path.join(workspaceDir, "memory");
  const sessionsDir = resolveSessionsDir(workspaceDir);

  const now = event.timestamp;
  const dateStr = now.toISOString().split("T")[0];
  const timeStr = now.toISOString().split("T")[1].split(".")[0];
  const timeClean = timeStr.replace(/:/g, "");
  const source = (ctx.commandSource as string) || "unknown";
  const sessionEntry = (ctx.previousSessionEntry || ctx.sessionEntry || {}) as Record<string, unknown>;
  const sessionId = (sessionEntry.sessionId as string) || "unknown";

  // --- Also extract facts from the ending session ---
  const sessionFile = sessionEntry.sessionFile as string | undefined;
  let transcript = "";

  if (sessionFile) {
    log("Reading session for fact extraction on reset", { file: sessionFile.replace(os.homedir(), "~") });
    const result = await readRecentMessages(sessionFile, 30);
    transcript = result.raw;
  } else {
    const found = await findSessionFile(sessionsDir, sessionId);
    if (found) {
      const result = await readRecentMessages(found, 30);
      transcript = result.raw;
    }
  }

  // Extract facts via LLM
  const cfg = (ctx.cfg || {}) as Record<string, unknown>;
  const apiKey = resolveApiKey(cfg);
  const baseUrl = resolveBaseUrl(cfg);

  if (transcript) {
    const extractionModel = resolveExtractionModel(cfg);
    log("Extracting facts on session reset", { model: extractionModel, baseUrl, transcriptLen: transcript.length });
    const extractedFacts = await extractFacts(transcript, apiKey, extractionModel, baseUrl);
    if (extractedFacts) {
      const factLines = extractedFacts.split("\n").filter(l => l.trim());
      const factContent = [
        `# Extracted Facts — ${dateStr} ${timeStr} (/reset)`,
        "",
        `- **Session**: ${event.sessionKey}`,
        `- **Session ID**: ${sessionId}`,
        `- **Trigger**: /${event.action}`,
        "",
        "## Facts",
        "",
        ...factLines,
        "",
        "---",
        `_Auto-extracted by memory-flush hook on session reset_`,
        "",
      ].join("\n");

      const factFile = await writeFileSafe(memoryDir, `${dateStr}-facts-reset-${timeClean}.md`, factContent);
      log("Facts saved on reset", { file: factFile.replace(os.homedir(), "~"), factCount: factLines.length });
    } else {
      log("No facts extracted on reset");
    }
  } else {
    log("Skipping extraction on reset", { hasKey: !!apiKey, hasTranscript: !!transcript });
  }

  // Log the reset
  const logContent = [
    `# Session Reset Log — ${dateStr} ${timeStr}`,
    "",
    `- **Action**: /${event.action}`,
    `- **Session**: ${event.sessionKey}`,
    `- **Session ID**: ${sessionId}`,
    `- **Source**: ${source}`,
    "",
    "---",
    `_Auto-logged by memory-flush hook_`,
    "",
  ].join("\n");

  const filename = `${dateStr}-session-log.md`;
  await writeFileSafe(memoryDir, filename, logContent);
  log("Session reset logged", { action: event.action });
}

// --- Main Handler ---

const handler = async (event: {
  type: string;
  action: string;
  sessionKey: string;
  timestamp: Date;
  context: Record<string, unknown>;
  messages: string[];
}) => {
  try {
    if (event.type === "session" && event.action === "compact:before") {
      await onCompactBefore(event);
      return;
    }

    if (event.type === "command" && (event.action === "new" || event.action === "reset")) {
      await onCommandNew(event);
      return;
    }
  } catch (err) {
    log("Handler error", {
      type: event.type,
      action: event.action,
      error: err instanceof Error ? err.message : String(err),
    });
  }
};

export default handler;

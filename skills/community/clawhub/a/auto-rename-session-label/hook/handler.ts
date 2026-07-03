import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { glob } from "node:fs/promises";

// ─────────────────────────────────────────────────────────────────────────────
// auto-session-label — portable OpenClaw internal hook
//
// On `message:received`, give a not-yet-labeled session a short title generated
// by the SAME model the session is currently using. Falls back to truncating the
// first user message on any failure. No machine-specific paths or personal data:
// everything is resolved at runtime from the environment.
// ─────────────────────────────────────────────────────────────────────────────

const MAX_LABEL_LEN = 50; // fallback truncation length (chars)
const TITLE_MAX_LEN = 30; // LLM title hard cap (chars)
const LLM_TIMEOUT_MS = 15000;
const LLM_MAX_TOKENS = 1024; // must be generous: some proxied models emit no
// visible text and stop at "length" when this is too small.

// English instruction; the TITLE language must follow the user's own text.
const TITLE_INSTRUCTION = `You generate a short title for a chat session based on the user's first message.

Rules:
- Maximum 20 characters.
- Write the title in the SAME language as the user's message. Do not translate.
- Output ONLY the title text. No quotes, no trailing punctuation, no explanation.`;

// ── Runtime path resolution (no hardcoded machine paths) ─────────────────────
function openclawHome(): string {
  const env = process.env.OPENCLAW_HOME && process.env.OPENCLAW_HOME.trim();
  if (env) return env;
  return path.join(os.homedir(), ".openclaw");
}

// Derive the agent id from the event/sessionKey, else env, else "main".
// sessionKey looks like: agent:<agentId>:<surface>:<uuid>
function resolveAgentId(event: any): string {
  const ctxAgent = event?.context?.agentId;
  if (ctxAgent && String(ctxAgent).trim()) return String(ctxAgent).trim();
  const sk = event?.sessionKey ? String(event.sessionKey) : "";
  const m = sk.match(/^agent:([^:]+):/);
  if (m) return m[1];
  const envAgent = process.env.OPENCLAW_AGENT_ID && process.env.OPENCLAW_AGENT_ID.trim();
  if (envAgent) return envAgent;
  return "main";
}

function sessionsFileFor(agentId: string): string {
  return path.join(openclawHome(), "agents", agentId, "sessions", "sessions.json");
}

function configFile(): string {
  return path.join(openclawHome(), "openclaw.json");
}

function agentDirFor(agentId: string): string {
  return path.join(openclawHome(), "agents", agentId);
}

// Locate the installed OpenClaw `dist` directory. Tries several candidates so
// this works regardless of how OpenClaw was installed (npm -g, nvm, etc.).
let cachedDistDir: string | null | undefined;
function distDir(): string | null {
  if (cachedDistDir !== undefined) return cachedDistDir;
  const candidates: string[] = [];

  // 1) Relative to the running CLI / node entry, if available.
  for (const p of [process.env.OPENCLAW_DIST, process.argv[1], process.execPath]) {
    if (!p) continue;
    try {
      let dir = fs.statSync(p).isDirectory() ? p : path.dirname(p);
      for (let i = 0; i < 6; i++) {
        const d = path.join(dir, "dist");
        if (fs.existsSync(path.join(d, "package.json")) || hasHashed(d)) {
          candidates.push(d);
          break;
        }
        const parent = path.dirname(dir);
        if (parent === dir) break;
        dir = parent;
      }
    } catch {}
  }

  // 2) Common global install roots.
  const home = os.homedir();
  for (const root of [
    process.env.npm_config_prefix && path.join(process.env.npm_config_prefix, "lib", "node_modules"),
    path.join(home, ".npm-global", "lib", "node_modules"),
    "/usr/local/lib/node_modules",
    "/usr/lib/node_modules",
    "/opt/homebrew/lib/node_modules",
  ]) {
    if (!root) continue;
    candidates.push(path.join(root, "openclaw", "dist"));
  }

  for (const d of candidates) {
    if (d && hasHashed(d)) {
      cachedDistDir = d;
      return d;
    }
  }
  cachedDistDir = null;
  return null;
}

// Quick check that a dir looks like an OpenClaw dist (has hashed stream bundle).
function hasHashed(dir: string): boolean {
  try {
    if (!fs.existsSync(dir)) return false;
    const files = fs.readdirSync(dir);
    return files.some((f) => /^stream-.*\.js$/.test(f));
  } catch {
    return false;
  }
}

// ── Read first user message (works across transcript schema variants) ────────
function getFirstUserMessage(sessionFile: string): string | null {
  try {
    const content = fs.readFileSync(sessionFile, "utf8");
    for (const line of content.split("\n")) {
      if (!line.trim()) continue;
      let entry: any;
      try { entry = JSON.parse(line); } catch { continue; }
      if (entry === null) continue;
      const msg = entry.message;
      const role = entry.role || (msg && msg.role);
      const type = entry.type || (msg && msg.type);
      const text =
        entry.text ||
        (msg && msg.text) ||
        (msg && typeof msg.content === "string" ? msg.content : null) ||
        (entry.content && typeof entry.content === "string" ? entry.content : null);
      if ((role === "user" || type === "user") && text && text.trim()) {
        return text.trim();
      }
    }
  } catch {}
  return null;
}

function truncateFallback(text: string): string {
  const t = text.trim();
  const trimmed = t.slice(0, MAX_LABEL_LEN);
  return trimmed.length < t.length ? trimmed + "…" : trimmed;
}

function cleanTitle(raw: string | null): string | null {
  if (!raw) return null;
  let t = String(raw).trim();
  t = t.replace(/^["'「『《\s]+|["'」』》\s]+$/g, "").replace(/\s+/g, " ").trim();
  if (!t) return null;
  return t.slice(0, TITLE_MAX_LEN);
}

// ── Resolve the REAL provider id (sessions.json may store an alias) ──────────
function resolveRealProvider(cfg: any, sessModel: string, sessProvider?: string): string | null {
  const providers = cfg?.models?.providers || {};
  if (sessProvider && providers[sessProvider]) {
    const ms = providers[sessProvider].models || [];
    if (ms.some((m: any) => m.id === sessModel)) return sessProvider;
  }
  for (const [pid, p] of Object.entries<any>(providers)) {
    const ms = p?.models || [];
    if (ms.some((m: any) => m.id === sessModel)) return pid;
  }
  return null;
}

// ── Locate a hashed dist module exporting a given symbol (version-resilient) ──
async function importDistExport(dist: string, globPattern: string, name: string): Promise<any> {
  const re = new RegExp("\\b" + name + " as (\\w+)");
  for await (const file of glob(path.join(dist, globPattern))) {
    let src: string;
    try { src = fs.readFileSync(file, "utf8"); } catch { continue; }
    const m = src.match(re);
    if (m) {
      const mod = await import(file);
      const fn = mod[m[1]] || mod[name];
      if (typeof fn === "function") return fn;
    }
  }
  return null;
}

// ── Generate a title via the OpenClaw internal completeSimple chain ──────────
// Uses the SAME provider/model as the session. Returns null on any failure.
async function generateTitle(cfg: any, agentDir: string, provider: string, model: string, userMessage: string): Promise<string | null> {
  const dist = distDir();
  if (!dist) return null;

  const [resolveModelAsync, prepareModelForSimpleCompletion, getRuntimeAuthForModel, requireApiKey, applyPreparedRuntimeAuthToModel, completeSimple] =
    await Promise.all([
      importDistExport(dist, "model-*.js", "resolveModelAsync"),
      importDistExport(dist, "simple-completion-transport-*.js", "prepareModelForSimpleCompletion"),
      importDistExport(dist, "runtime-model-auth.runtime-*.js", "getRuntimeAuthForModel"),
      importDistExport(dist, "model-auth-runtime-shared-*.js", "requireApiKey"),
      importDistExport(dist, "provider-request-config-*.js", "applyPreparedRuntimeAuthToModel"),
      importDistExport(dist, "stream-*.js", "completeSimple"),
    ]);

  if (!resolveModelAsync || !prepareModelForSimpleCompletion || !getRuntimeAuthForModel ||
      !requireApiKey || !applyPreparedRuntimeAuthToModel || !completeSimple) {
    return null;
  }

  const resolved = await resolveModelAsync(provider, model, agentDir, cfg);
  if (!resolved?.model) return null;

  const completionModel = prepareModelForSimpleCompletion({ model: resolved.model, cfg });
  const runtimeAuth = await getRuntimeAuthForModel({ model: completionModel, cfg, workspaceDir: agentDir });
  const apiKey = requireApiKey(runtimeAuth, provider);
  const runtimeModel = applyPreparedRuntimeAuthToModel(completionModel, runtimeAuth);

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), LLM_TIMEOUT_MS);
  try {
    // Inline the instruction into the user message: some upstream proxies reject
    // a separate system message ("System messages are not allowed").
    const combined = `${TITLE_INSTRUCTION}\n\n---\nUser's first message:\n${userMessage}`;
    const result = await completeSimple(runtimeModel, {
      messages: [{ role: "user", content: combined, timestamp: Date.now() }],
    }, {
      apiKey,
      maxTokens: LLM_MAX_TOKENS,
      temperature: 0.3,
      signal: controller.signal,
    });
    if (result?.stopReason === "error") return null;
    const text = (result?.content || [])
      .filter((b: any) => b.type === "text")
      .map((b: any) => b.text)
      .join("")
      .trim();
    return cleanTitle(text);
  } finally {
    clearTimeout(timer);
  }
}

// ── Hook entry ───────────────────────────────────────────────────────────────
export default async function handler(event: any) {
  if (event.type !== "message" || event.action !== "received") return;

  const sessionKey = event.sessionKey;
  if (!sessionKey) return;

  const agentId = resolveAgentId(event);
  const sessionsFile = sessionsFileFor(agentId);

  let sessions: any;
  try {
    sessions = JSON.parse(fs.readFileSync(sessionsFile, "utf8"));
  } catch { return; }

  const sess = sessions[sessionKey];
  if (!sess) return;
  if (sess.label && String(sess.label).trim()) return; // already labeled → skip
  if (!sess.sessionFile) return;

  // First user message: prefer the instant event context, else read transcript.
  const ctxContent = event.context?.content ? String(event.context.content).trim() : null;
  const firstMsg = ctxContent || getFirstUserMessage(sess.sessionFile);
  if (!firstMsg) return;

  let label: string | null = null;

  // Try an LLM title with the CURRENT session model; fall back on any failure.
  try {
    const cfg = JSON.parse(fs.readFileSync(configFile(), "utf8"));
    const sessModel = sess.modelOverride || sess.model;
    const sessProvider = sess.providerOverride || sess.modelProvider;
    if (sessModel) {
      const provider = resolveRealProvider(cfg, sessModel, sessProvider);
      if (provider) {
        label = await generateTitle(cfg, agentDirFor(agentId), provider, sessModel, firstMsg);
      }
    }
  } catch {
    label = null;
  }

  // Fallback: legacy truncation of the first user message.
  if (!label) label = truncateFallback(firstMsg);
  if (!label) return;

  // Re-read sessions.json right before write to avoid clobbering concurrent updates.
  try {
    const fresh = JSON.parse(fs.readFileSync(sessionsFile, "utf8"));
    const target = fresh[sessionKey];
    if (!target) return;
    if (target.label && String(target.label).trim()) return; // labeled meanwhile
    target.label = label;
    fs.writeFileSync(sessionsFile, JSON.stringify(fresh, null, 2), "utf8");
  } catch {}
}

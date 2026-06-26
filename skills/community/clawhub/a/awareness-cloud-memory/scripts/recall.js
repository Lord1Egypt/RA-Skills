#!/usr/bin/env node
// ---------------------------------------------------------------------------
// UserPromptSubmit hook — Auto-recall: search memory and inject context
// Protocol: receives JSON on stdin, outputs context text on stdout
// ---------------------------------------------------------------------------

const { loadConfig, resolveEndpoint, apiGet, apiPost, readStdin } = require("./shared");

// ---------------------------------------------------------------------------
// Keyword extraction (zero LLM cost)
// ---------------------------------------------------------------------------

function extractKeywords(text, max = 8) {
  if (!text) return "";
  const tokens = [];
  for (const m of text.matchAll(/["](.*?)[""]/g)) tokens.push(m[1]);
  for (const m of text.matchAll(/[\w.-]+\.(?:py|js|ts|tsx|json|md|sql|go|rs|java|sh)\b/gi)) tokens.push(m[0]);
  for (const m of text.matchAll(/\b[A-Z][A-Z0-9_]{1,15}\b/g)) tokens.push(m[0]);
  for (const m of text.matchAll(/\b[a-z]+(?:[A-Z][a-z0-9]+)+\b/g)) tokens.push(m[0]);
  for (const m of text.matchAll(/\b[a-z][a-z0-9]*(?:[-_][a-z0-9]+)+\b/g)) tokens.push(m[0]);
  const seen = new Set();
  const result = [];
  for (const t of tokens) {
    const k = t.trim().toLowerCase();
    if (k.length < 2 || seen.has(k)) continue;
    seen.add(k);
    result.push(t.trim());
    if (result.length >= max) break;
  }
  return result.join(" ");
}

function esc(s) {
  return String(s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  let input = {};
  try { input = await readStdin(); } catch { /* no stdin */ }

  const prompt = input.prompt || "";
  if (!prompt) process.exit(0);

  const config = loadConfig();
  const ep = await resolveEndpoint(config);
  if (!ep) process.exit(0);

  try {
    // Load session context
    const params = new URLSearchParams({
      days: "7",
      max_cards: String(config.recallLimit),
      max_tasks: String(config.recallLimit),
    });
    if (config.agentRole) params.set("agent_role", config.agentRole);
    const ctx = await apiGet(ep.baseUrl, ep.apiKey, `/memories/${ep.memoryId}/context`, params);

    // Semantic + keyword search
    const keywords = extractKeywords(prompt);
    const recall = await apiPost(ep.baseUrl, ep.apiKey, `/memories/${ep.memoryId}/retrieve`, {
      query: prompt,
      keyword_query: keywords || undefined,
      custom_kwargs: {
        limit: config.recallLimit,
        use_hybrid_search: true,
        reconstruct_chunks: true,
        recall_mode: "hybrid",
        vector_weight: 0.7,
        full_text_weight: 0.3,
      },
      include_installed: true,
      agent_role: config.agentRole || undefined,
      detail: "summary",
    });

    // Build XML memory block
    const parts = ["<awareness-memory>"];

    const skills = ctx.active_skills || [];
    if (skills.length > 0) {
      parts.push("  <skills>");
      for (const s of skills) {
        parts.push(`    <skill title="${esc(s.title)}">`);
        if (s.summary) parts.push(`      ${s.summary}`);
        parts.push("    </skill>");
      }
      parts.push("  </skills>");
    }

    const sessions = ctx.last_sessions || [];
    if (sessions.length > 0) {
      parts.push("  <last-sessions>");
      for (const s of sessions) {
        parts.push(`    <session date="${esc(s.date)}" events="${s.event_count || 0}">${esc(s.summary)}</session>`);
      }
      parts.push("  </last-sessions>");
    }

    const days = ctx.recent_days || [];
    if (days.length > 0) {
      parts.push("  <recent-progress>");
      for (const d of days) {
        if (d.narrative) parts.push(`    <day date="${esc(d.date)}">${esc(d.narrative)}</day>`);
      }
      parts.push("  </recent-progress>");
    }

    const attn = ctx.attention_summary;
    if (attn?.needs_attention) {
      parts.push("  <attention-protocol>");
      parts.push(`    <summary stale_tasks="${attn.stale_tasks || 0}" high_risks="${attn.high_risks || 0}" />`);
      parts.push("  </attention-protocol>");
    }

    const tasks = ctx.open_tasks || [];
    if (tasks.length > 0) {
      parts.push("  <open-tasks>");
      for (const t of tasks) {
        parts.push(`    <task priority="${t.priority || "medium"}" status="${t.status || "pending"}">${esc(t.title)}</task>`);
      }
      parts.push("  </open-tasks>");
    }

    const cards = ctx.knowledge_cards || [];
    if (cards.length > 0) {
      parts.push("  <knowledge>");
      for (const c of cards) {
        parts.push(`    <card category="${esc(c.category)}">${esc(c.title)}: ${esc(c.summary)}</card>`);
      }
      parts.push("  </knowledge>");
    }

    const results = (recall.results || []).filter((r) => !r.score || r.score >= 0.5);
    if (results.length > 0) {
      parts.push("  <recall>");
      for (const r of results) {
        if (r.content) {
          const score = r.score ? ` score="${r.score.toFixed(3)}"` : "";
          parts.push(`    <result${score}>${r.content}</result>`);
        }
      }
      parts.push("  </recall>");
    }

    parts.push("</awareness-memory>");
    process.stdout.write(parts.join("\n"));
  } catch (err) {
    process.stderr.write(`[awareness] recall failed: ${err.message}\n`);
  }
}

main().catch(() => process.exit(0));

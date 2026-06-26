#!/usr/bin/env node
// ⚠️ DO NOT EDIT — auto-generated from sdks/_shared/scripts/save-memory.js
// Edit the source in sdks/_shared/scripts/ then run:
//   bash scripts/sync-shared-scripts.sh
// See docs/features/f-036/shared-scripts-consolidation.md

// ---------------------------------------------------------------------------
// save-memory.js — Simple wrapper for Claude to save memories via Bash
// Usage: node save-memory.js '{"content":"what happened","cards":[{"title":"...","summary":"...","category":"decision"}]}'
// ---------------------------------------------------------------------------

const { loadConfig, resolveEndpoint, mcpCall } = require("./shared");

async function main() {
  const arg = process.argv[2];
  if (!arg) { process.stderr.write("Usage: node save-memory.js '{json}'\n"); process.exit(1); }

  let data;
  try { data = JSON.parse(arg); } catch (e) {
    process.stderr.write(`[awareness] JSON parse error: ${e.message}\n`);
    process.exit(1);
  }

  const config = loadConfig();
  const ep = await resolveEndpoint(config);
  if (!ep) { process.stderr.write("[awareness] daemon not available\n"); process.exit(1); }

  const insights = {};
  if (data.cards && data.cards.length > 0) {
    insights.knowledge_cards = data.cards.map(c => ({
      title: c.title || "",
      summary: c.summary || "",
      category: c.category || "key_point",
      confidence: c.confidence || 0.85,
    }));
  }
  if (data.tasks && data.tasks.length > 0) {
    insights.action_items = data.tasks.map(t => ({
      title: t.title || "",
      description: t.description || "",
      priority: t.priority || "medium",
    }));
  }

  try {
    const result = await mcpCall(ep.localUrl, "awareness_record", {
      action: "remember",
      content: data.content || "",
      insights: Object.keys(insights).length > 0 ? insights : undefined,
    }, 8000);

    // Cache perception signals for recall.js to surface on next prompt
    const perception = result.perception?.perception || result.perception;
    if (perception && Array.isArray(perception) && perception.length > 0) {
      try {
        const fs = require("fs");
        const path = require("path");
        const projectAwareness = path.join(path.resolve(process.env.PWD || process.cwd()), ".awareness");
        const cacheDir = fs.existsSync(projectAwareness) ? projectAwareness : path.join(process.env.HOME || "", ".awareness");
        if (!fs.existsSync(cacheDir)) fs.mkdirSync(cacheDir, { recursive: true });
        const cacheFile = path.join(cacheDir, "perception-cache.json");
        // Append to existing cache (keep last 10 signals max)
        let existing = [];
        try { existing = JSON.parse(fs.readFileSync(cacheFile, "utf8")); } catch { /* empty */ }
        const updated = [...perception.map(s => ({ ...s, _ts: Date.now() })), ...existing].slice(0, 10);
        fs.writeFileSync(cacheFile, JSON.stringify(updated), "utf8");
      } catch { /* best-effort, never fail the save */ }
    }

    process.stdout.write(JSON.stringify({ status: "saved", id: result.id }) + "\n");
  } catch (err) {
    process.stderr.write(`[awareness] save failed: ${err.message}\n`);
    process.exit(1);
  }
}

main().catch(() => process.exit(1));

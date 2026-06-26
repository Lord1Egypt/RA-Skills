/**
 * Shared Harness Builder — canonical XML context format for Awareness Memory.
 * Used by both Claude Code skill (recall.js) and OpenClaw plugin (hooks.ts)
 * as fallback when server-side rendered_context is not available.
 *
 * Zero LLM. Pure template rendering.
 */

/**
 * Escape XML special characters.
 * @param {string} s
 * @returns {string}
 */
export function escapeXml(s) {
  if (!s) return "";
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

/**
 * Extract keywords from user prompt for hybrid search.
 * Merges CC's basic extraction with OpenClaw's enhanced CJK support.
 * @param {string} text - User prompt text
 * @param {number} max - Maximum keywords to extract (default 8)
 * @returns {string[]}
 */
export function extractKeywords(text, max = 8) {
  if (!text || typeof text !== "string") return [];
  const kws = new Set();

  // Quoted strings (including smart quotes)
  for (const m of text.matchAll(/[""\u201c]([^"\u201d]{2,40})["\u201d]/g)) {
    kws.add(m[1].trim());
  }

  // File patterns (comprehensive: 20+ extensions)
  for (const m of text.matchAll(
    /[\w./-]+\.(py|js|ts|tsx|jsx|json|md|sql|go|rs|java|sh|yml|yaml|csv|xlsx|pdf|toml|cfg|conf|xml|html|css|txt|log|mjs|mts)\b/gi
  )) {
    kws.add(m[0]);
  }

  // UPPER_CASE constants
  for (const m of text.matchAll(/\b[A-Z][A-Z_]{2,}\b/g)) {
    kws.add(m[0]);
  }

  // camelCase / PascalCase identifiers
  for (const m of text.matchAll(/\b[a-z][a-zA-Z]{4,}\b/g)) {
    kws.add(m[0]);
  }

  // snake_case identifiers
  for (const m of text.matchAll(/\b[a-z]+_[a-z_]+\b/g)) {
    kws.add(m[0]);
  }

  // CJK names and titles (2-4 chars)
  for (const m of text.matchAll(/[\u4e00-\u9fff]{2,4}/g)) {
    kws.add(m[0]);
  }

  // Version numbers and issue references
  for (const m of text.matchAll(/[#vV]?\d[\d.,:-]+\w*/g)) {
    if (m[0].length > 1) kws.add(m[0]);
  }

  return [...kws].slice(0, max);
}

/**
 * Estimate token count for a string.
 * CJK chars ~1.5 chars/token, ASCII ~4 chars/token, mixed ~2.5.
 * @param {string} s
 * @returns {number}
 */
function estimateTokens(s) {
  if (!s) return 0;
  const cjk = (s.match(/[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]/g) || []).length;
  const rest = s.length - cjk;
  return Math.ceil(cjk / 1.5 + rest / 4);
}

/**
 * Build a section's items, respecting a token budget.
 * Returns { lines: string[], tokens: number, count: number }.
 * Items are added in order (assumed pre-sorted by relevance) until budget is spent.
 * @param {object[]} items - Source items
 * @param {function} renderFn - (item) => string (the XML line)
 * @param {number} budget - Max tokens for this section
 * @returns {{ lines: string[], tokens: number, count: number }}
 */
function buildSection(items, renderFn, budget) {
  const lines = [];
  let tokens = 0;
  let count = 0;
  for (const item of items) {
    const line = renderFn(item);
    const cost = estimateTokens(line);
    if (tokens + cost > budget && count > 0) break; // always include at least 1
    lines.push(line);
    tokens += cost;
    count++;
  }
  return { lines, tokens, count };
}

// Default token budget and per-section allocation ratios.
// Sections with higher priority get their budget first; lower-priority sections
// share whatever remains. Total default: 20000 tokens.
const DEFAULT_TOKEN_BUDGET = 20000;
const SECTION_CONFIG = [
  // { key, priority (lower=higher), budgetRatio (share of total) }
  { key: 'perception', priority: 1, budgetRatio: 0.05 },
  { key: 'knowledge',  priority: 2, budgetRatio: 0.25 },
  { key: 'recall',     priority: 3, budgetRatio: 0.30 },
  { key: 'tasks',      priority: 4, budgetRatio: 0.10 },
  { key: 'prefs',      priority: 5, budgetRatio: 0.08 },
  { key: 'progress',   priority: 6, budgetRatio: 0.12 },
  { key: 'sessions',   priority: 7, budgetRatio: 0.10 },
];

/**
 * Build the canonical <awareness-memory> XML block.
 * Uses a token budget (default 20k) to dynamically control how many items
 * from each section are included. Content is never truncated — only the
 * number of items per section is adjusted to fit the budget.
 *
 * @param {object} ctx - Init context (from awareness_init response)
 * @param {object[]} [recallResults] - Recall search results
 * @param {object[]} [perceptionSignals] - Cached perception signals
 * @param {object} [options] - Additional options
 * @param {string} [options.recordRuleScript] - Path to save-memory.js (CC only)
 * @param {string} [options.localUrl] - Local daemon URL for dashboard
 * @param {number} [options.tokenBudget] - Max tokens for memory context (default 20000)
 * @returns {string}
 */
export function buildContextXml(ctx, recallResults, perceptionSignals, options = {}) {
  const esc = escapeXml;
  const totalBudget = options.tokenBudget || DEFAULT_TOKEN_BUDGET;
  const parts = ["<awareness-memory>"];

  if (options.currentFocus) {
    parts.push("  <current-focus>");
    parts.push(`    ${esc(String(options.currentFocus))}`);
    parts.push("  </current-focus>");
  }

  // Fixed-cost sections (skills, attention, dashboard, record-rule) are small
  // and always included. We reserve ~500 tokens for them.
  const fixedReserve = 500;
  const dynamicBudget = totalBudget - fixedReserve;

  // --- Skills (always full, tiny) ---
  const skills = ctx.active_skills || [];
  if (skills.length > 0) {
    parts.push("  <skills>");
    for (const skill of skills) {
      parts.push(`    <skill title="${esc(skill.title || "")}">${esc(skill.summary || "")}</skill>`);
    }
    parts.push("  </skills>");
  }

  // --- Prepare all section data + renderers ---
  const sectionData = {
    perception: perceptionSignals || [],
    knowledge:  (ctx.context || ctx).knowledge_cards || [],
    recall:     recallResults || [],
    tasks:      (ctx.context || ctx).open_tasks || [],
    prefs:      ctx.user_preferences || [],
    progress:   ((ctx.context || ctx).recent_days || []).filter(d => d.narrative),
    sessions:   (ctx.context || ctx).last_sessions || ctx.recent_sessions || [],
  };

  const renderers = {
    perception: (s) =>
      `    <signal type="${esc(s.type || "")}">${esc(s.message || "")}</signal>`,
    knowledge: (c) => {
      const rule = (c.actionable_rule || "").trim();
      const content = rule ? esc(rule) : `${esc(c.title || "")}: ${esc(c.summary || "")}`;
      return `    <card category="${esc(c.category || "")}">${content}</card>`;
    },
    recall: (r) => {
      const score = r.score || 0;
      const content = esc(r.content || "");
      let daysAgo = 0;
      if (r.created_at) {
        try { daysAgo = Math.floor((Date.now() - new Date(r.created_at).getTime()) / 86400000); } catch {}
      }
      if (score > 0.8 && daysAgo > 3) {
        return `    <aha score="${score.toFixed(2)}" days-ago="${daysAgo}">${content}</aha>`;
      }
      const scoreAttr = score ? ` score="${score.toFixed(2)}"` : "";
      return `    <result${scoreAttr}>${content}</result>`;
    },
    tasks: (t) =>
      `    <task priority="${esc(t.priority || "medium")}" status="${esc(t.status || "pending")}">${esc(t.title || "")}</task>`,
    prefs: (p) => {
      const rule = (p.actionable_rule || "").trim();
      const content = rule ? esc(rule) : `${esc(p.title || "")}: ${esc(p.summary || "")}`;
      return `    <pref category="${esc(p.category || "")}">${content}</pref>`;
    },
    progress: (day) =>
      `    <day date="${esc(day.date || "")}">${esc(day.narrative || "")}</day>`,
    sessions: (s) => {
      const date = esc(s.date || "");
      const events = s.event_count || s.memory_count || 0;
      const summary = esc(s.summary || "");
      return `    <session date="${date}" events="${events}">${summary}</session>`;
    },
  };

  // --- Phase 1: build each section with its allocated budget ---
  const sectionResults = {};
  let usedTokens = 0;

  for (const cfg of SECTION_CONFIG) {
    const sectionBudget = Math.floor(dynamicBudget * cfg.budgetRatio);
    sectionResults[cfg.key] = buildSection(sectionData[cfg.key], renderers[cfg.key], sectionBudget);
    usedTokens += sectionResults[cfg.key].tokens;
  }

  // --- Phase 2: redistribute unused budget to high-priority sections that were cut ---
  let remaining = dynamicBudget - usedTokens;
  for (const cfg of SECTION_CONFIG) {
    if (remaining <= 200) break;
    const sr = sectionResults[cfg.key];
    if (sr.count >= sectionData[cfg.key].length) continue; // not truncated
    const rebuilt = buildSection(sectionData[cfg.key], renderers[cfg.key], sr.tokens + remaining);
    remaining -= (rebuilt.tokens - sr.tokens);
    sectionResults[cfg.key] = rebuilt;
  }

  // --- Render sections in display order ---
  if (sectionResults.prefs.lines.length > 0) {
    parts.push("  <who-you-are>");
    parts.push(...sectionResults.prefs.lines);
    parts.push("  </who-you-are>");
  }

  if (sectionResults.sessions.lines.length > 0) {
    parts.push("  <last-sessions>");
    parts.push(...sectionResults.sessions.lines);
    parts.push("  </last-sessions>");
  }

  if (sectionResults.progress.lines.length > 0) {
    parts.push("  <recent-progress>");
    parts.push(...sectionResults.progress.lines);
    parts.push("  </recent-progress>");
  }

  // --- Attention Protocol (fixed cost, always included) ---
  const attn = (ctx.context || ctx).attention_summary || ctx.attention_summary || {};
  const stale = attn.stale_tasks || 0;
  const risks = attn.high_risks || 0;
  const totalOpen = attn.total_open_tasks || 0;
  parts.push("  <attention-protocol>");
  parts.push(`    <summary stale_tasks="${stale}" high_risks="${risks}" total_open="${totalOpen}" />`);
  if (stale > 0 || risks > 0) {
    parts.push("    <instructions>");
    parts.push("      Review all open tasks and risks below. For stale tasks (pending > 3 days), remind the user or suggest completion/removal.");
    parts.push("      For high risks, warn the user before starting work. Update resolved items via awareness_record.");
    parts.push("    </instructions>");
  }
  parts.push("  </attention-protocol>");

  if (sectionResults.tasks.lines.length > 0) {
    parts.push("  <open-tasks>");
    parts.push(...sectionResults.tasks.lines);
    parts.push("  </open-tasks>");
  }

  if (sectionResults.knowledge.lines.length > 0) {
    parts.push("  <knowledge>");
    parts.push(...sectionResults.knowledge.lines);
    parts.push("  </knowledge>");
  }

  if (sectionResults.recall.lines.length > 0) {
    parts.push("  <recall>");
    parts.push(...sectionResults.recall.lines);
    parts.push("  </recall>");
  }

  if (sectionResults.perception.lines.length > 0) {
    parts.push("  <perception>");
    parts.push("    <action-required>BEFORE responding to the user, you MUST address each signal below. "
      + "For contradictions: inform the user and ask if intentional. "
      + "For resonance: mention the related past experience. "
      + "For patterns: suggest a systematic fix. "
      + "For staleness: warn knowledge may be outdated. "
      + "For guards: STOP and warn about the known pitfall.</action-required>");
    parts.push(...sectionResults.perception.lines);
    parts.push("  </perception>");
  }

  // --- Dashboard (local mode, optional) ---
  if (options.localUrl) {
    parts.push(`  <dashboard>Memory is running locally. View at ${esc(options.localUrl)}</dashboard>`);
  }

  // --- Record Rule (CC skill only, optional) ---
  // F-056 — body composed from atomic templates in sdks/_shared/prompts/*.md
  // via scripts/sync-shared-prompts.mjs. Edit the .md files, not the lines
  // between the SHARED markers below.
  if (options.recordRuleScript) {
    const recordRule = `  <record-rule>
    Save significant work SILENTLY: node "${esc(options.recordRuleScript)}" '<JSON>'
    JSON: {"content":"what+why in detail","cards":[...],"skills":[...]}
    <!-- SHARED:extraction-when-to-extract BEGIN -->
- The user **made a decision** — chose X over Y, with a stated reason
- A **non-obvious bug was fixed** — symptom + root cause + fix + how to avoid recurring
- A **workflow / convention was established** — ordered steps, preconditions, gotchas
- The user stated a **preference or hard constraint** — "I prefer X", "never do Y"
- A **pitfall was encountered and a workaround found** — trigger + impact + avoidance
- An **important fact about the user or project** surfaced for the first time
<!-- SHARED:extraction-when-to-extract END -->
    <!-- SHARED:extraction-when-not-to-extract BEGIN -->
- **Agent framework metadata**: content beginning with \`Sender (untrusted metadata)\`,
  \`turn_brief\`, \`[Operational context metadata ...]\`, \`[Subagent Context]\`, or wrapped
  inside \`Request:\` / \`Result:\` / \`Send:\` envelopes that only carry such metadata.
  Strip those wrappers mentally and judge what remains.
- **Greetings / command invocations**: "hi", "run tests", "save this", "try again".
- **"What can you do" / AI self-introduction turns**.
- **Code restatement**: code itself lives in git; only extract the *lesson* if one exists.
- **Test / debug sessions where the user is verifying the tool works** (including tests
  of awareness_record / awareness_recall themselves). A bug fix in those tools IS worth
  extracting as problem_solution; a raw "let me test if recall works" turn is not.
- **Transient status / progress updates** — "building...", "retrying...", "✅ done".

The single question to ask: **"If I start a fresh project 6 months from now, will being
reminded of this content materially help me?"** If not, do not emit a card.
Returning \`"knowledge_cards": []\` is a **first-class answer** — prefer it over fabricating
a card from low-signal content.
<!-- SHARED:extraction-when-not-to-extract END -->
    <!-- SHARED:extraction-scoring BEGIN -->
Every card you emit MUST carry three LLM self-assessed scores (0.0-1.0):

- \`novelty_score\`: how new is this vs known facts & existing cards?
  (restating an existing card = 0.1; a fresh decision = 0.9)
- \`durability_score\`: will this still matter in 6 months? (transient debug state = 0.1;
  architectural decision or user preference = 0.9)
- \`specificity_score\`: is there concrete substance — file paths, commands, error strings,
  version numbers, exact function names? (vague platitude = 0.1; reproducible recipe = 0.9)

The daemon will discard any card where \`novelty_score < 0.4\` OR \`durability_score < 0.4\`.
This is intentional — score honestly. Under-extraction is much better than noise.
<!-- SHARED:extraction-scoring END -->
    <!-- SHARED:extraction-quality-gate BEGIN -->
Drop the card rather than submit if it would fail any of these:

- **R1 length**: \`summary\` ≥ 80 chars (technical: decision / problem_solution
  / workflow / pitfall / insight / key_point); ≥ 40 chars (personal:
  personal_preference / important_detail / plan_intention /
  activity_preference / health_info / career_info / custom_misc).
- **R2 no duplication**: \`summary\` not byte-identical to \`title\`.
- **R3 no envelope leakage**: neither \`title\` nor \`summary\` starts with
  \`Request:\`, \`Result:\`, \`Send:\`, \`Sender (untrusted metadata)\`,
  \`[Operational context metadata\`, or \`[Subagent Context]\`.
- **R4 no placeholder tokens**: \`summary\` has no \`TODO\`, \`FIXME\`,
  \`lorem ipsum\`, \`example.com\`, or literal \`placeholder\`.
- **R5 Markdown on long summaries**: ≥ 200 chars → use bullets /
  \`inline code\` / **bold**. Soft.

**Recall-friendliness** — without these, a card is "accepted but
invisible" at retrieval time:

- **R6 grep-friendly title**: at least one concrete term you'd search
  for — product (\`pgvector\`), file (\`daemon.mjs\`), error, version,
  function (\`_submitInsights\`), project noun. Vague titles ("Decision
  made", "Bug fixed", "决定") score ~30 % precision@3.
  ❌ "Bug fixed"  ✅ "Fix pgvector dim 1536→1024 mismatch".
- **R7 topic-specific tags**: 3-5 tags, each a specific
  noun/product/concept. Never \`general\`, \`note\`, \`misc\`, \`fix\`,
  \`project\`, \`tech\`. ❌ \`["general","note"]\`  ✅ \`["pgvector","vector-db","cost"]\`.
- **R8 multilingual keyword diversity**: concepts that have both EN +
  CJK names → include BOTH in the summary at least once. Example:
  "用 \`pgvector\` 做向量数据库存储" matches queries in either language.

Rejected cards return in \`response.cards_skipped[]\`. R6-R8 are
warnings, not blocks — use them to self-critique before submitting.
<!-- SHARED:extraction-quality-gate END -->
    <!-- SHARED:skill-extraction BEGIN -->
A \`skill\` is a **reusable procedure the user will invoke again** (e.g. "publish
SDK to npm", "regenerate golden snapshots after schema change"). Skills go in
\`insights.skills[]\`, NOT \`insights.knowledge_cards[]\`.

Emit a skill when ALL three hold:
1. The content describes a **repeated** procedure (2+ earlier cards mention
   the same steps, or the user explicitly says "this is our workflow for X").
2. There is a **stable trigger** you can name — the task / state that makes
   someone reach for this skill.
3. The steps are **executable without improvisation** — concrete files,
   commands, flags, verification signals. "Do it carefully" fails this bar.

Skip (return empty \`skills: []\`) for:
- Single debugging incidents → \`problem_solution\` card instead.
- Generic advice with no concrete steps.
- Configuration snapshots → \`important_detail\` card instead.

Required shape per skill:
\`\`\`json
{
  "name": "3-8 words, action-oriented (\\"Publish SDK to npm\\")",
  "summary": "200-500 chars of second-person imperative — pasteable into an agent prompt. Include WHY in one clause so the agent knows when to deviate.",
  "methods": [{"step": 1, "description": "≥20 chars, names a file/command/flag — no vague verbs"}],
  "pitfalls": ["One-line known failure mode + how to avoid it (e.g. 'npm mirror rejects publish — always pass --registry=https://registry.npmjs.org/')"],
  "verification": ["One-line post-run check (e.g. 'Run \`npm view <pkg> version\` — should match the bumped version')"],
  "trigger_conditions": [{"pattern": "When publishing @awareness-sdk/*", "weight": 0.9}],
  "tags": ["npm", "publish", "release"],
  "reusability_score": 0.0,
  "durability_score": 0.0,
  "specificity_score": 0.0
}
\`\`\`

MANDATORY content bars (daemon scores on 8 dims; skills below 28/40 are
hidden from active_skills[]):
- **≥ 1 pitfall** with a concrete avoidance — NOT "be careful"
- **≥ 1 verification** line with a checkable signal (command output, file
  exists, HTTP 200, etc.) — NOT "check that it worked"
- **Every step mentions a concrete token**: file path, command, flag,
  version number, or URL. "Update the config" fails; "Edit \`foo.json\` and
  bump \`version\` field" passes.
- ≥ 3 steps, ≥ 2 trigger patterns, 3-8 tags, all three scores ≥ 0.5.

Discard if these cannot be satisfied — emitting a vague skill pollutes the
TOC that future agents pick from.
<!-- SHARED:skill-extraction END -->
    Categories (pick ONE, ask: is this about the USER or about TECH?):
      Personal: personal_preference, important_detail, career_info, activity_preference, plan_intention, health_info, custom_misc
      Technical: decision, problem_solution, workflow, pitfall, insight, key_point
  </record-rule>`;
    parts.push(recordRule);
  }

  parts.push("</awareness-memory>");
  return parts.join("\n");
}

/**
 * Parse recall results from various response formats into a filtered array.
 * Handles: MCP text (JSON string), plain text, or JSON object with .results.
 * @param {object|string|null} recall - Raw recall response
 * @returns {object[]} Filtered results array
 */
export function parseRecallResults(recall) {
  if (!recall) return [];
  if (typeof recall === "string") {
    try {
      const parsed = JSON.parse(recall);
      return (parsed.results || parsed.items || []).filter(r => !r.score || r.score >= 0.4);
    } catch {
      if (recall.trim().length > 20) {
        return [{ content: recall.trim(), score: 0.5 }];
      }
      return [];
    }
  }
  return (recall.results || []).filter(r => !r.score || r.score >= 0.5);
}

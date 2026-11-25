#!/usr/bin/env node
// geo-audit-lite — offline AI-search readiness (GEO) audit for saved files.
// Reads --html/--robots/--llms files, never touches the network.
// JSON report on stdout. Exit 0 = all pass/info, 1 = warns/fails, 2 = usage/read error.
import fs from "node:fs";

/* ---------------- robots.txt ---------------- */

const AI_BOTS = [
  { engine: "ChatGPT search", bots: ["oai-searchbot", "chatgpt-user"] },
  { engine: "OpenAI training", bots: ["gptbot"] },
  { engine: "Claude", bots: ["claudebot", "claude-user", "claude-searchbot"] },
  { engine: "Perplexity", bots: ["perplexitybot", "perplexity-user"] },
  { engine: "Google AI", bots: ["googlebot"] },
];
const TRAINING_ONLY = new Set(["gptbot", "claudebot"]);

function parseRobots(text) {
  const groups = [];
  const sitemaps = [];
  let cur = { uas: [], allow: [], disallow: [] };
  let hasRules = false;
  for (const raw of text.split("\n")) {
    const line = raw.replace(/#.*$/, "").trim();
    const m = line.match(/^([a-z-]+)\s*:\s*(\S*)/i);
    if (!m) continue;
    const field = m[1].toLowerCase();
    const value = m[2].trim();
    if (field === "user-agent") {
      if (hasRules) {
        groups.push(cur);
        cur = { uas: [], allow: [], disallow: [] };
        hasRules = false;
      }
      cur.uas.push(value.toLowerCase());
    } else if (field === "sitemap") {
      sitemaps.push(value);
    } else if (field === "allow" || field === "disallow") {
      if (!cur.uas.length) continue;
      cur[field].push(value);
      hasRules = true;
    }
  }
  if (cur.uas.length) groups.push(cur);
  return { groups, sitemaps };
}

function botAccess(bot, groups) {
  const g =
    groups.find((gr) => gr.uas.includes(bot)) ??
    groups.find((gr) => gr.uas.includes("*"));
  if (!g) return "unlisted";
  if (g.disallow.includes("/") && !g.allow.includes("/")) return "blocked";
  return "allowed";
}

/* ---------------- html helpers ---------------- */

const tagAttr = (html, re) => {
  const m = html.match(re);
  return m ? (m[1] ?? m[0]).trim() : null;
};
const count = (html, re) => (html.match(re) || []).length;

function stripTags(html) {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ");
}

function jsonLdTypes(html) {
  const types = new Set();
  let hasDate = false;
  let hasAuthor = false;
  let bad = 0;
  const walk = (n) => {
    if (Array.isArray(n)) return n.forEach(walk);
    if (!n || typeof n !== "object") return;
    const t = n["@type"];
    if (typeof t === "string") types.add(t);
    if (Array.isArray(t)) t.forEach((x) => types.add(String(x)));
    if ("datePublished" in n || "dateModified" in n) hasDate = true;
    if ("author" in n || "publisher" in n) hasAuthor = true;
    Object.values(n).forEach(walk);
  };
  for (const m of html.matchAll(
    /<script[^>]+type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi,
  )) {
    try {
      walk(JSON.parse(m[1]));
    } catch {
      bad++;
    }
  }
  return { types, hasDate, hasAuthor, bad };
}

/* ---------------- audit ---------------- */

export function audit({ html = null, robots = null, llms = null }) {
  const checks = [];
  const c = (id, status, detail) => checks.push({ id, status, detail });

  if (robots) {
    const { groups, sitemaps } = parseRobots(robots);
    const blocked = [];
    const detail = [];
    for (const e of AI_BOTS) {
      const sts = e.bots.map((b) => botAccess(b, groups));
      e.bots.forEach((b, i) => sts[i] === "blocked" && blocked.push(b));
      detail.push(
        `${e.engine}: ${sts.includes("blocked") ? "BLOCKED" : sts.includes("unlisted") ? "not listed" : "open"}`,
      );
    }
    const critical = blocked.filter((b) => !TRAINING_ONLY.has(b));
    c(
      "ai-crawler-access",
      critical.length ? "fail" : "pass",
      critical.length
        ? `Blocked: ${blocked.join(", ")}. Fix — append per-bot groups: ` +
            critical.map((b) => `User-agent: ${b} / Allow: /`).join("; ")
        : detail.join(" · ") +
            (blocked.length ? " (training-only blocks — fine if intentional)" : ""),
    );
    c(
      "sitemap-declared",
      sitemaps.length ? "pass" : "warn",
      sitemaps.length
        ? `Sitemap: ${sitemaps[0]}`
        : "No Sitemap: directive in robots.txt.",
    );
  } else {
    c("robots-txt", "info", "robots.txt not provided — crawler access unchecked.");
  }

  if (html) {
    const title = tagAttr(html, /<title[^>]*>([^<]*)<\/title>/i);
    if (!title) c("title", "fail", "No <title> element.");
    else if (title.length > 65)
      c("title", "warn", `Title length ${title.length} (aim ≤65 chars).`);
    else c("title", "pass", `Title ok (${title.length} chars).`);

    const desc =
      tagAttr(html, /<meta[^>]+name=["']description["'][^>]+content=["']([^"']*)["']/i) ??
      tagAttr(html, /<meta[^>]+content=["']([^"']*)["'][^>]+name=["']description["']/i);
    c(
      "meta-description",
      desc ? "pass" : "warn",
      desc ? `Description ok (${desc.length} chars).` : "Missing meta description.",
    );

    const canonical = tagAttr(html, /<link[^>]+rel=["']canonical["'][^>]+href=["']([^"']+)["']/i);
    c("canonical", canonical ? "pass" : "warn",
      canonical ? `Canonical: ${canonical}` : "No canonical link tag.");

    const h1 = count(html, /<h1[\s>]/gi);
    c("single-h1", h1 === 1 ? "pass" : "warn",
      h1 === 1 ? "Exactly one <h1>." : `${h1} <h1> elements — one clear claim per page.`);

    const { types, hasDate, hasAuthor, bad } = jsonLdTypes(html);
    c(
      "json-ld",
      types.size ? "pass" : "fail",
      types.size
        ? `Types: ${[...types].slice(0, 6).join(", ")}${types.size > 6 ? "…" : ""}${bad ? ` (${bad} malformed block(s))` : ""}`
        : "No JSON-LD — add Organization/Article/FAQPage markup.",
    );
    c(
      "faq-schema",
      types.has("FAQPage") ? "pass" : "warn",
      types.has("FAQPage")
        ? "FAQPage markup present."
        : "No FAQPage schema — Q&A blocks are the most-quoted format.",
    );

    const qHeads = count(html, /<h[23][^>]*>[^<]*\?\s*<\/h[23]>/gi);
    c("question-headings", qHeads >= 2 ? "pass" : "warn",
      `${qHeads} question-format H2/H3 — match how users prompt AI.`);

    const firstP = tagAttr(html, /<p[^>]*>([^<]{1,})<\/p>/i) ?? "";
    const answerish = firstP.length >= 40 && firstP.length <= 400;
    c("answer-first", answerish ? "pass" : "warn",
      firstP
        ? `Opening paragraph ${firstP.length} chars — ${answerish ? "direct answer" : "aim 40–400 chars of declarative text"}.`
        : "No <p> found — lead with a 1–2 sentence direct answer.");

    const tables = count(html, /<table[\s>]/gi);
    const lists = count(html, /<[uo]l[\s>]/gi);
    const words = stripTags(html).split(/\s+/).filter(Boolean).length;
    c("extractable-content",
      words >= 300 && (tables || lists) ? "pass" : "warn",
      `${words} words, ${tables} tables, ${lists} lists — engines lift structured, substantive content.`);

    const timeEls = count(html, /<time[^>]+datetime=/gi);
    c("freshness", hasDate || timeEls ? "pass" : "warn",
      hasDate
        ? "datePublished/dateModified in JSON-LD."
        : timeEls
          ? `${timeEls} <time datetime> elements.`
          : "No dates found — engines prefer fresh, dated sources.");

    c("authorship", hasAuthor ? "pass" : "warn",
      hasAuthor
        ? "author/publisher declared in JSON-LD."
        : "No author or publisher entity — attribution helps engines trust the source.");
  } else {
    c("page-html", "info", "HTML not provided — content checks skipped.");
  }

  if (llms) {
    const hasH1 = /^#\s+\S/m.test(llms);
    const hasQuote = /^>\s+\S/m.test(llms);
    const links = (llms.match(/\]\(https?:\/\//g) ?? []).length;
    c("llms-txt", hasH1 && links > 0 ? "pass" : "warn",
      `${links} links${hasH1 ? "" : ", missing # title"}${hasQuote ? "" : ", missing > summary"}.`);
  } else {
    c("llms-txt", "warn", "No /llms.txt provided — a markdown index of canonical pages for AI crawlers.");
  }

  return checks;
}

export function summarize(checks) {
  const summary = { pass: 0, warn: 0, fail: 0, info: 0 };
  for (const ch of checks) summary[ch.status]++;
  return summary;
}

// Evidence in the supplied files that only the full version's live fetches
// would resolve. Returns [] when nothing applies.
export function upgradeReasons({ html = null, robots = null, llms = null } = {}) {
  const reasons = [];
  if (html && /<link[^>]+rel=["']canonical["'][^>]+href=["']https?:\/\//i.test(html))
    reasons.push(
      "page declares an absolute canonical URL — the full version fetches live URLs to confirm what AI crawlers actually receive",
    );
  if (robots && /^sitemap\s*:/im.test(robots))
    reasons.push(
      "robots.txt declares a Sitemap URL — the full version fetches and validates it live",
    );
  if (llms) {
    const links = (llms.match(/\]\(https?:\/\//g) ?? []).length;
    if (links)
      reasons.push(
        `llms.txt lists ${links} outbound link(s) — the full version validates them live`,
      );
  }
  return reasons;
}

const isMain =
  process.argv[1] &&
  (import.meta.url ===
    new URL(`file:///${process.argv[1].replace(/\\/g, "/")}`).href ||
    process.argv[1].endsWith("audit.js"));
if (isMain) {
  const args = process.argv.slice(2);
  const files = {};
  for (let i = 0; i < args.length - 1; i += 2) {
    const key = args[i].replace(/^--/, "");
    if (["html", "robots", "llms"].includes(key)) files[key] = args[i + 1];
  }
  if (!Object.keys(files).length) {
    console.error(
      "usage: node audit.js [--html page.html] [--robots robots.txt] [--llms llms.txt]",
    );
    process.exit(2);
  }
  const input = {};
  try {
    for (const [k, f] of Object.entries(files)) input[k] = fs.readFileSync(f, "utf8");
  } catch (e) {
    console.error(`cannot read input file: ${e.message}`);
    process.exit(2);
  }
  const checks = audit(input);
  const summary = summarize(checks);
  const report = { summary, checks };
  const reasons = upgradeReasons(input);
  if (reasons.length) report.upgrade = { skill: "geo-audit", reasons };
  console.log(JSON.stringify(report, null, 2));
  process.exit(summary.warn + summary.fail > 0 ? 1 : 0);
}

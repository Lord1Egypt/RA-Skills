#!/usr/bin/env node
/**
 * EIGEN AI TERMINAL — MCP SERVER v1.0 (ClawHub Edition)
 *
 * Clean build for ClawHub distribution.
 * Fetches public read-only data from terminal.clawlab.dev.
 * No local file access. No secrets. No user data collected.
 */
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
// ── Data Loading ────────────────────────────────────────────
let cachedData = null;
let cachedHistory = null;
let cachedManifest = null;
let dataCacheTime = 0;
let historyCacheTime = 0;
let manifestCacheTime = 0;
const CACHE_TTL = 5 * 60 * 1000;
const DATA_URL = "https://terminal.clawlab.dev/data";
const WIKI_URL = "https://terminal.clawlab.dev/wiki";
function readLocalFile(..._candidates) { return null; }
function dataFileCandidates(_filename) { return []; }
function wikiFileCandidates(_filePath) { return []; }
async function loadData() {
    const now = Date.now();
    if (cachedData && now - dataCacheTime < CACHE_TTL)
        return cachedData;
    const local = readLocalFile(...dataFileCandidates("radar.json"));
    if (local) {
        cachedData = JSON.parse(local);
        dataCacheTime = now;
        return cachedData;
    }
    const res = await fetch(`${DATA_URL}/radar.json`);
    cachedData = (await res.json());
    dataCacheTime = now;
    return cachedData;
}
async function loadHistory() {
    const now = Date.now();
    if (cachedHistory && now - historyCacheTime < CACHE_TTL)
        return cachedHistory;
    const local = readLocalFile(...dataFileCandidates("history.json"));
    if (local) {
        cachedHistory = JSON.parse(local);
        historyCacheTime = now;
        return cachedHistory;
    }
    try {
        const res = await fetch(`${DATA_URL}/history.json`);
        if (res.ok) {
            cachedHistory = (await res.json());
            historyCacheTime = now;
            return cachedHistory;
        }
    }
    catch {
        /* fall through */
    }
    return [];
}
async function loadManifest() {
    const now = Date.now();
    if (cachedManifest && now - manifestCacheTime < CACHE_TTL)
        return cachedManifest;
    const local = readLocalFile(...wikiFileCandidates("manifest.json"));
    if (local) {
        cachedManifest = JSON.parse(local);
        manifestCacheTime = now;
        return cachedManifest;
    }
    const res = await fetch(`${WIKI_URL}/manifest.json`);
    cachedManifest = (await res.json());
    manifestCacheTime = now;
    return cachedManifest;
}
async function readWikiFile(filePath) {
    const local = readLocalFile(...wikiFileCandidates(filePath));
    if (local)
        return local;
    try {
        const res = await fetch(`${WIKI_URL}/${filePath}`);
        if (res.ok)
            return await res.text();
    }
    catch {
        /* fall through */
    }
    return null;
}
// ── Formatting ──────────────────────────────────────────────
const DOMAIN_NAMES = {
    "frontier-models": "Frontier Models",
    "open-source-models": "Open Source Models",
    "compute-hardware": "Compute & Hardware",
    "ai-agents": "AI Agents",
    "ai-coding-tools": "AI Coding Tools",
    "ai-infrastructure": "AI Infrastructure",
    "ai-safety-alignment": "AI Safety",
    "ai-policy-regulation": "AI Policy & Regulation",
    "ai-business-funding": "AI Business & Funding",
    "multimodal-ai": "Multimodal AI",
    "ai-for-science": "AI for Science",
    "robotics-embodied-ai": "Robotics & Embodied AI",
    "ai-research-breakthroughs": "Research Breakthroughs",
    "edge-on-device-ai": "Edge & On-Device AI",
    "ai-in-enterprise": "AI in Enterprise",
    "frontier-edges": "Unsolved Problems",
};
function dn(id) {
    return DOMAIN_NAMES[id] || id;
}
function fmtDate(d) {
    try {
        return new Date(d).toLocaleDateString("en-US", {
            month: "long",
            day: "numeric",
            year: "numeric",
        });
    }
    catch {
        return d;
    }
}
function fmtSignal(s, significance) {
    const domains = s.nodeNames?.length > 0
        ? s.nodeNames.join(", ")
        : s.nodes.map(dn).join(", ");
    const actionable = s.practical !== false ? "Yes" : "No";
    const tags = s.tags?.length ? `\nTags: ${s.tags.join(", ")}` : "";
    const action = s.actionLine ? `\n**Why it matters:** ${s.actionLine}` : "";
    return [
        `### ${s.title}`,
        `Domains: ${domains} | Significance: ${significance} | Actionable: ${actionable}${tags}`,
        action,
        s.description,
        s.source ? `\nSource: ${s.source}` : "",
    ]
        .filter(Boolean)
        .join("\n");
}
function fmtRipple(r) {
    const parts = [];
    if (r.chains?.length) {
        parts.push("**What this causes:**");
        for (const c of r.chains)
            parts.push(`- ${c.title} (${c.direction}, ${c.strength}): ${c.mechanism}`);
    }
    if (r.convergences?.length) {
        parts.push("**Trends this feeds:**");
        for (const c of r.convergences)
            parts.push(`- ${c.title} (${c.confidence} confidence): ${c.predictedOutcome}`);
    }
    if (r.bottlenecks?.length) {
        parts.push("**Blocked by:**");
        for (const b of r.bottlenecks)
            parts.push(`- ${b.title} [${b.status}]: ${b.summary}`);
    }
    if (r.predictions?.length) {
        parts.push("**Predictions:**");
        for (const p of r.predictions)
            parts.push(`- ${p.title} (${p.confidence}, check by ${p.checkDate})`);
    }
    return parts.join("\n");
}
/** Broad keyword match — used for retrieval only. The agent does semantic filtering. */
function matches(text, query) {
    const words = query
        .toLowerCase()
        .split(/\s+/)
        .filter((w) => w.length >= 2);
    const t = text.toLowerCase();
    return words.some((w) => t.includes(w));
}
/** Count how many query words appear — higher = better match */
function matchStrength(text, query) {
    const words = query
        .toLowerCase()
        .split(/\s+/)
        .filter((w) => w.length >= 3);
    const t = text.toLowerCase();
    let hits = 0;
    for (const w of words)
        if (t.includes(w))
            hits++;
    return hits;
}
function txt(text) {
    return { content: [{ type: "text", text }] };
}
// ── MCP Server ──────────────────────────────────────────────
const server = new McpServer({
    name: "eigen-ai-terminal",
    version: "1.0.0",
});
// ─── today ──────────────────────────────────────────────────
server.tool("today", "Get today's AI intelligence — all signals from the latest scan with significance levels, domains, actionability flag, and tags. The agent should use its knowledge of the user to decide what to surface. For the morning brief, pick 2-3 actionable items. Returns ripple effects for significant signals.", {
    significance: z
        .enum(["all", "significant", "notable", "breakthrough"])
        .default("all")
        .describe("Filter by significance. 'significant' = major developments. 'notable' = worth knowing. 'breakthrough' = rare, industry-changing."),
    only_actionable: z
        .boolean()
        .default(false)
        .describe("If true, only return actionable signals (practical for builders)"),
}, async ({ significance, only_actionable }) => {
    const data = await loadData();
    const all = [];
    if (significance === "all" || significance === "breakthrough")
        (data.brief.breakthrough || []).forEach((s, i) => all.push({ signal: s, sig: "breakthrough", idx: i }));
    if (significance === "all" || significance === "significant")
        data.brief.significant.forEach((s, i) => all.push({ signal: s, sig: "significant", idx: i }));
    if (significance === "all" || significance === "notable")
        data.brief.notable.forEach((s, i) => all.push({ signal: s, sig: "notable", idx: i }));
    const items = only_actionable
        ? all.filter(({ signal }) => signal.practical !== false)
        : all;
    const lines = [
        `# Today's AI Intelligence — ${fmtDate(data.brief.date)}`,
        `${data.brief.signalsTotal} signals scanned | ${data.brief.signalsSignificant} significant | ${data.brief.signalsBreakthrough || 0} breakthrough`,
        "",
    ];
    const grouped = {};
    for (const item of items) {
        (grouped[item.sig] ??= []).push(item);
    }
    for (const level of ["breakthrough", "significant", "notable"]) {
        const group = grouped[level];
        if (!group?.length)
            continue;
        lines.push(`## ${level[0].toUpperCase() + level.slice(1)}`);
        lines.push("");
        for (const { signal, sig, idx } of group) {
            lines.push(fmtSignal(signal, sig));
            if (sig === "significant" || sig === "breakthrough") {
                const ripple = data.ripples?.significant?.[idx];
                if (ripple) {
                    lines.push("");
                    lines.push(fmtRipple(ripple));
                }
            }
            lines.push("", "---", "");
        }
    }
    lines.push('Use about("[topic]") to go deeper on any signal. Use changes() to check for updates later.');
    return txt(lines.join("\n"));
});
// ─── about ──────────────────────────────────────────────────
server.tool("about", "Get everything we know about a topic, company, model, technology, or AI domain — all in one call. Returns: wiki content, recent signals, related trends, blockers, and predictions. Use when the user asks about something specific. Examples: about('Anthropic'), about('MCP'), about('AI coding tools'), about('open source models').", {
    topic: z
        .string()
        .describe("What to look up — a company, model, technology, concept, or AI domain"),
}, async ({ topic }) => {
    const data = await loadData();
    const manifest = await loadManifest();
    const topicLower = topic.toLowerCase();
    const lines = [
        `# About: ${topic}`,
        `As of ${fmtDate(data.brief.date)}`,
        "",
    ];
    let foundContent = false;
    // 1. Entity page or node page
    const entityHit = data.entityIndex
        ? Object.entries(data.entityIndex).find(([name]) => name.toLowerCase().includes(topicLower) ||
            topicLower.includes(name.toLowerCase()))
        : undefined;
    const filesToTry = [];
    if (entityHit)
        filesToTry.push(entityHit[1]);
    // Also search manifest
    for (const f of manifest.files) {
        const name = (f.frontmatter.name || "").toLowerCase();
        const fp = f.path.toLowerCase();
        if (name.includes(topicLower) ||
            fp.includes(topicLower.replace(/\s+/g, "-"))) {
            if (!filesToTry.includes(f.path))
                filesToTry.push(f.path);
        }
    }
    for (const fp of filesToTry.slice(0, 2)) {
        const raw = await readWikiFile(fp);
        if (!raw)
            continue;
        foundContent = true;
        const label = fp.startsWith("nodes/")
            ? "Domain Overview"
            : fp.startsWith("entities/")
                ? "Entity Profile"
                : "Knowledge Base";
        const stripped = raw.replace(/^---[\s\S]*?---\n*/, "");
        lines.push(`## ${label}`);
        lines.push(stripped.slice(0, 3000));
        lines.push("");
        break; // only show the best match
    }
    // 2. Matching signals
    const allSignals = [
        ...data.brief.significant.map((s, i) => ({
            ...s,
            sig: "significant",
            idx: i,
        })),
        ...data.brief.notable.map((s, i) => ({
            ...s,
            sig: "notable",
            idx: i,
        })),
    ];
    const hitSignals = allSignals.filter((s) => matches(s.title +
        " " +
        s.description +
        " " +
        (s.tags || []).join(" ") +
        " " +
        s.nodes.map(dn).join(" "), topic));
    if (hitSignals.length > 0) {
        foundContent = true;
        lines.push("## Recent Signals");
        for (const s of hitSignals.slice(0, 5)) {
            lines.push(fmtSignal(s, s.sig));
            if (s.sig === "significant") {
                const ripple = data.ripples?.significant?.[s.idx];
                if (ripple) {
                    lines.push("");
                    lines.push(fmtRipple(ripple));
                }
            }
            lines.push("");
        }
    }
    // 3. Matching trends
    const hitTrends = data.convergences.filter((c) => matches(c.title +
        " " +
        c.predictedOutcome +
        " " +
        c.forces.map((f) => f.description + " " + dn(f.origin)).join(" "), topic));
    if (hitTrends.length > 0) {
        foundContent = true;
        lines.push("## Developing Trends");
        for (const t of hitTrends) {
            lines.push(`### ${t.title}`);
            lines.push(`Confidence: ${t.confidence} | Timeline: ${t.timeline || "uncertain"}`);
            lines.push(t.predictedOutcome);
            if (t.forces.length > 0) {
                lines.push("Contributing forces:");
                for (const f of t.forces)
                    lines.push(`- ${f.description} (from ${dn(f.origin)})`);
            }
            if (t.invalidation)
                lines.push(`Would be disproved by: ${t.invalidation}`);
            lines.push("");
        }
    }
    // 4. Matching blockers
    const hitBlocked = data.bottlenecks.filter((b) => matches(b.title + " " + b.summary + " " + b.blocks.map(dn).join(" "), topic));
    if (hitBlocked.length > 0) {
        foundContent = true;
        lines.push("## What's Blocked");
        for (const b of hitBlocked) {
            lines.push(`### ${b.title}`);
            lines.push(`Status: ${b.status} | Blocks: ${b.blocks.map(dn).join(", ")}`);
            lines.push(b.summary);
            lines.push(`${b.attackers} teams working on this | ${b.looseningSignals} signs of progress`);
            lines.push("");
        }
    }
    // 5. Matching predictions
    const hitPreds = data.predictions.filter((p) => matches(p.title + " " + (p.basedOn || ""), topic));
    if (hitPreds.length > 0) {
        foundContent = true;
        lines.push("## Predictions");
        for (const p of hitPreds)
            lines.push(`- **${p.title}** — ${p.confidence} confidence, check by ${p.checkDate}`);
        lines.push("");
    }
    // 6. Related wiki pages
    const relatedPages = manifest.files
        .filter((f) => {
        const name = (f.frontmatter.name || "").toLowerCase();
        return (f.tags.some((t) => t.toLowerCase().includes(topicLower)) ||
            f.wikilinks.some((l) => l.toLowerCase().includes(topicLower)) ||
            name.includes(topicLower));
    })
        .filter((f) => !filesToTry.includes(f.path))
        .slice(0, 5);
    if (relatedPages.length > 0) {
        lines.push("## Related Pages");
        for (const p of relatedPages) {
            const name = p.frontmatter.name || p.path;
            lines.push(`- ${name} → read("${p.path}")`);
        }
        lines.push("");
    }
    if (!foundContent) {
        lines.push("No information found for this topic. Try a different name or broader term.");
        lines.push(`Available domains: ${Object.values(DOMAIN_NAMES).join(", ")}`);
    }
    return txt(lines.join("\n"));
});
// ─── ripple ─────────────────────────────────────────────────
server.tool("ripple", "Trace the cause-and-effect chain of a specific signal — what it pushes, what trends it feeds, what blocks it, and what we predict next. Pass the signal title or a keyword to match. Use when the user asks 'what does this mean?' or 'what happens because of this?'", {
    signal: z
        .string()
        .describe("The signal title or a keyword to match against today's signals"),
}, async ({ signal }) => {
    const data = await loadData();
    const all = [
        ...data.brief.significant.map((s, i) => ({ ...s, sig: "significant", idx: i })),
        ...data.brief.notable.map((s, i) => ({ ...s, sig: "notable", idx: i })),
    ];
    // Find best match
    const queryLower = signal.toLowerCase();
    let matched = all.find((s) => s.title.toLowerCase().includes(queryLower)) ||
        all.sort((a, b) => matchStrength(b.title + " " + b.description, signal) -
            matchStrength(a.title + " " + a.description, signal))[0];
    if (!matched || matchStrength(matched.title + " " + matched.description, signal) === 0) {
        return txt(`No signal matching "${signal}".\n\nToday's signals:\n${all.map((s) => `- ${s.title}`).join("\n")}`);
    }
    const lines = [
        `# Ripple Effects: ${matched.title}`,
        `Significance: ${matched.sig}`,
        "",
        matched.description,
        "",
    ];
    const ripple = matched.sig === "significant"
        ? data.ripples?.significant?.[matched.idx]
        : data.ripples?.notable?.[matched.idx];
    if (ripple) {
        lines.push(fmtRipple(ripple));
    }
    else {
        // Build connections from shared domains
        const sigNodes = new Set(matched.nodes);
        const relTrends = data.convergences.filter((c) => c.forces.some((f) => sigNodes.has(f.origin)));
        const relBlocked = data.bottlenecks.filter((b) => b.blocks.some((x) => sigNodes.has(x)));
        const relChains = data.forceChains.filter((fc) => fc.status === "active" &&
            fc.targets.some((t) => sigNodes.has(t)));
        if (relChains.length > 0) {
            lines.push("**What this causes:**");
            for (const c of relChains.slice(0, 3))
                lines.push(`- ${c.title} (${c.direction}): ${c.mechanism.slice(0, 250)}`);
            lines.push("");
        }
        if (relTrends.length > 0) {
            lines.push("**Trends this connects to:**");
            for (const t of relTrends)
                lines.push(`- ${t.title} (${t.confidence} confidence): ${t.predictedOutcome}`);
            lines.push("");
        }
        if (relBlocked.length > 0) {
            lines.push("**Blocked by:**");
            for (const b of relBlocked)
                lines.push(`- ${b.title} [${b.status}]: ${b.summary}`);
            lines.push("");
        }
        if (relChains.length === 0 &&
            relTrends.length === 0 &&
            relBlocked.length === 0) {
            lines.push("No mapped ripple effects for this signal yet.");
        }
    }
    lines.push("");
    lines.push(`Use about("${matched.nodes[0] ? dn(matched.nodes[0]) : signal}") for broader context.`);
    return txt(lines.join("\n"));
});
// ─── trends ─────────────────────────────────────────────────
server.tool("trends", "Get developing trends in AI — patterns where 3+ independent signals point at the same outcome. Each trend has contributing forces from different domains, a confidence level, a timeline, and what would disprove it. Use when the user asks 'what trends should I watch?' or wants forward-looking context.", {}, async () => {
    const data = await loadData();
    // Sort: high confidence first
    const confRank = {
        high: 4,
        "medium-high": 3,
        medium: 2,
        forming: 1,
        low: 0,
    };
    const sorted = [...data.convergences].sort((a, b) => (confRank[b.confidence.toLowerCase()] ?? 1) -
        (confRank[a.confidence.toLowerCase()] ?? 1));
    const lines = [
        "# Developing Trends in AI",
        `${sorted.length} active trends tracked | As of ${fmtDate(data.brief.date)}`,
        "",
    ];
    for (const t of sorted) {
        lines.push(`## ${t.title}`);
        lines.push(`Confidence: ${t.confidence} | Timeline: ${t.timeline || "uncertain"}`);
        lines.push("");
        lines.push(`**What we think will happen:** ${t.predictedOutcome}`);
        lines.push("");
        if (t.forces.length > 0) {
            lines.push("**Why we think this:**");
            for (const f of t.forces)
                lines.push(`- ${f.description} (from ${dn(f.origin)}, ${f.strength})`);
            lines.push("");
        }
        if (t.invalidation)
            lines.push(`**What would disprove this:** ${t.invalidation}`);
        lines.push("", "---", "");
    }
    return txt(lines.join("\n"));
});
// ─── blocked ────────────────────────────────────────────────
server.tool("blocked", "Get what's holding AI progress back — constraints affecting multiple areas at once. Shows what's blocked, who's working on it, and signs of progress. Use when the user asks about limitations, risks, or 'what's the catch?'", {}, async () => {
    const data = await loadData();
    const lines = [
        "# What's Blocked in AI",
        `${data.bottlenecks.length} active blockers tracked`,
        "",
    ];
    for (const b of data.bottlenecks) {
        lines.push(`## ${b.title}`);
        lines.push(`Status: ${b.status} | Type: ${b.type || "constraint"}`);
        lines.push(`Blocks: ${b.blocks.map(dn).join(", ")}`);
        lines.push("");
        lines.push(b.summary || "No summary available.");
        lines.push("");
        lines.push(`${b.attackers} teams/companies working on this | ${b.looseningSignals} signs of progress`);
        lines.push("", "---", "");
    }
    return txt(lines.join("\n"));
});
// ─── speed ──────────────────────────────────────────────────
server.tool("speed", "Get rate-of-change metrics — how fast key things in AI are moving. Costs, capabilities, adoption, capital. Use when the user needs quantitative context, asks 'how fast is X changing?', or wants to understand momentum.", {
    category: z
        .enum(["all", "cost", "capability", "capital", "adoption"])
        .default("all")
        .describe("Filter: cost (pricing), capability (model performance), capital (funding), adoption (usage growth)"),
}, async ({ category }) => {
    const data = await loadData();
    const catMap = {
        cost: "Cost & Economics",
        capability: "Capability",
        capital: "Capital",
        adoption: "Adoption",
    };
    const filtered = category === "all"
        ? data.velocity
        : data.velocity.filter((v) => v.category === catMap[category]);
    const lines = [
        "# How Fast Things Are Moving",
        `${filtered.length} metrics tracked`,
        "",
    ];
    const groups = {};
    for (const v of filtered)
        (groups[v.category || "Other"] ??= []).push(v);
    for (const [cat, metrics] of Object.entries(groups)) {
        lines.push(`## ${cat}`);
        for (const v of metrics) {
            lines.push(`- **${v.metric}**: ${v.currentValue}`);
            lines.push(`  Rate of change: ${v.velocity} | Acceleration: ${v.acceleration}`);
            if (v.date)
                lines.push(`  Last measured: ${v.date}`);
        }
        lines.push("");
    }
    return txt(lines.join("\n"));
});
// ─── predictions ────────────────────────────────────────────
server.tool("predictions", "Get specific, dated predictions about where AI is heading — each with a confidence level and check date. We track whether they come true. Use when the user wants forward-looking context or asks 'what's coming next?'", {}, async () => {
    const data = await loadData();
    // Soonest check date first
    const sorted = [...data.predictions].sort((a, b) => {
        try {
            return (new Date(a.checkDate).getTime() -
                new Date(b.checkDate).getTime());
        }
        catch {
            return 0;
        }
    });
    const lines = [
        "# Predictions We're Tracking",
        `${sorted.length} active predictions`,
        "",
    ];
    for (const p of sorted) {
        lines.push(`## ${p.title}`);
        lines.push(`Confidence: ${p.confidence} | Check by: ${p.checkDate}`);
        if (p.basedOn)
            lines.push(`Based on: ${p.basedOn}`);
        lines.push("");
    }
    return txt(lines.join("\n"));
});
// ─── search ─────────────────────────────────────────────────
server.tool("search", "Search across the entire knowledge base — domain trackers, company profiles, daily briefs, frameworks. Returns matching files with context snippets. Use when looking for specific info or when about() didn't find enough.", {
    query: z
        .string()
        .describe("What to search for — a company, technology, concept, model name, or keyword"),
    max_results: z
        .number()
        .default(10)
        .describe("Maximum results to return"),
}, async ({ query, max_results }) => {
    const manifest = await loadManifest();
    const queryLower = query.toLowerCase();
    const queryWords = queryLower
        .split(/\s+/)
        .filter((w) => w.length >= 3);
    const scored = await Promise.all(manifest.files.map(async (f) => {
        let score = 0;
        const name = (f.frontmatter.name || "").toLowerCase();
        if (name.includes(queryLower))
            score += 10;
        if (f.tags.some((t) => t.toLowerCase().includes(queryLower)))
            score += 5;
        if (f.wikilinks.some((l) => l.toLowerCase().includes(queryLower)))
            score += 3;
        if (f.path
            .toLowerCase()
            .includes(queryLower.replace(/\s+/g, "-")))
            score += 5;
        // Partial word matching for broader retrieval
        if (score === 0) {
            for (const w of queryWords) {
                if (name.includes(w) || f.path.toLowerCase().includes(w))
                    score += 2;
            }
        }
        let snippet = "";
        if (score > 0) {
            const raw = await readWikiFile(f.path);
            if (raw) {
                if (raw.toLowerCase().includes(queryLower))
                    score += 5;
                for (const line of raw.split("\n")) {
                    const ll = line.toLowerCase();
                    if (ll.includes(queryLower) ||
                        queryWords.some((w) => ll.includes(w))) {
                        snippet = line.trim().slice(0, 250);
                        score += 2;
                        break;
                    }
                }
            }
        }
        return { ...f, score, snippet };
    }));
    const results = scored
        .filter((r) => r.score > 0)
        .sort((a, b) => b.score - a.score)
        .slice(0, max_results);
    if (results.length === 0) {
        return txt(`No results for "${query}". Try broader terms.\nAvailable domains: ${Object.values(DOMAIN_NAMES).join(", ")}`);
    }
    const lines = [
        `# Search: "${query}" — ${results.length} results`,
        "",
    ];
    for (const r of results) {
        const name = r.frontmatter.name || r.path;
        lines.push(`## ${name}`);
        lines.push(`Path: ${r.path}`);
        if (r.snippet)
            lines.push(`> ${r.snippet}`);
        if (r.tags.length)
            lines.push(`Tags: ${r.tags.join(", ")}`);
        lines.push(`→ read("${r.path}") for the full page`);
        lines.push("");
    }
    return txt(lines.join("\n"));
});
// ─── read ───────────────────────────────────────────────────
server.tool("read", "Read a specific page from the knowledge base. Returns full content with navigation links to related pages. Use after search() or about() points you to a file. Example paths: 'nodes/ai-agents.md', 'entities/anthropic.md', 'briefs/2026-04-08.md'.", {
    file_path: z
        .string()
        .describe("Path to the page, e.g. 'nodes/ai-agents.md'"),
}, async ({ file_path }) => {
    const raw = await readWikiFile(file_path);
    if (!raw) {
        const manifest = await loadManifest();
        const suggestions = manifest.files
            .filter((f) => f.path
            .toLowerCase()
            .includes(file_path.toLowerCase().replace(".md", "")))
            .slice(0, 5);
        const hint = suggestions.length > 0
            ? `\nDid you mean: ${suggestions.map((s) => s.path).join(", ")}?`
            : '\nUse search() to find what you\'re looking for.';
        return txt(`File not found: ${file_path}${hint}`);
    }
    const links = [
        ...new Set((raw.match(/\[\[([^\]]+)\]\]/g) || []).map((l) => l.replace(/\[\[|\]\]/g, ""))),
    ];
    const footer = links.length > 0
        ? `\n\n---\nRelated pages: ${links.join(", ")}\nUse read() or about() to explore any of these.`
        : "";
    return txt(raw + footer);
});
// ─── changes ────────────────────────────────────────────────
server.tool("changes", "Get what's new since a specific date. Returns new signals and updates. Use between morning briefs to check for breaking developments, or when the user hasn't checked in a while. If something significant is found, consider alerting the user proactively.", {
    since: z
        .string()
        .describe("Date to check from, e.g. '2026-04-07' or '2026-04-07T07:00:00Z'"),
}, async ({ since }) => {
    const sinceDate = new Date(since);
    const data = await loadData();
    const history = await loadHistory();
    const items = [];
    // Today's data
    const todayDate = new Date(data.brief.date);
    if (todayDate >= sinceDate) {
        for (const s of data.brief.significant || []) {
            items.push({
                date: data.brief.date,
                title: s.title,
                description: s.description,
                significance: "significant",
                domains: s.nodeNames?.length
                    ? s.nodeNames
                    : s.nodes.map(dn),
                source: s.source,
                practical: s.practical !== false,
            });
        }
        for (const s of data.brief.notable || []) {
            items.push({
                date: data.brief.date,
                title: s.title,
                description: s.description,
                significance: "notable",
                domains: s.nodeNames?.length
                    ? s.nodeNames
                    : s.nodes.map(dn),
                source: s.source,
                practical: s.practical !== false,
            });
        }
    }
    // Historical data
    for (const entry of history) {
        const d = new Date(entry.date);
        if (d >= sinceDate && entry.date !== data.brief.date) {
            for (const s of entry.signals)
                items.push({ date: entry.date, ...s });
        }
    }
    if (items.length === 0) {
        return txt(`No new signals since ${fmtDate(since)}. Check back later or use today() for the latest full scan.`);
    }
    // Sort: newest first, then by significance
    const sigRank = {
        breakthrough: 3,
        significant: 2,
        notable: 1,
    };
    items.sort((a, b) => {
        const dc = new Date(b.date).getTime() - new Date(a.date).getTime();
        if (dc !== 0)
            return dc;
        return (sigRank[b.significance] || 0) - (sigRank[a.significance] || 0);
    });
    const sigCount = items.filter((s) => s.significance === "significant" ||
        s.significance === "breakthrough").length;
    const lines = [
        `# Changes Since ${fmtDate(since)}`,
        `${items.length} new signals | ${sigCount} significant`,
        "",
    ];
    const sigItems = items.filter((s) => s.significance === "significant" ||
        s.significance === "breakthrough");
    if (sigItems.length > 0) {
        lines.push("## Significant");
        for (const s of sigItems) {
            lines.push(`### ${s.title}`);
            lines.push(`Date: ${s.date} | Domains: ${s.domains.join(", ")} | Actionable: ${s.practical ? "Yes" : "No"}`);
            lines.push(s.description.slice(0, 500));
            lines.push("");
        }
    }
    const notItems = items.filter((s) => s.significance === "notable");
    if (notItems.length > 0) {
        lines.push("## Notable");
        for (const s of notItems) {
            lines.push(`- **${s.title}** (${s.date}) — ${s.description.slice(0, 200)}`);
        }
        lines.push("");
    }
    lines.push('Use about("[topic]") to go deeper on any of these.');
    return txt(lines.join("\n"));
});
// ─── whats_new ──────────────────────────────────────────────
server.tool("whats_new", "Get the latest updates and tips for Eigen AI Terminal. Check during the morning brief — if there's something fresh, mention it casually in one line. Skip if nothing new.", {
    days: z
        .number()
        .default(7)
        .describe("How many days back to look"),
}, async ({ days }) => {
    let raw = await readWikiFile("whats-new.md");
    if (!raw) {
        // Fallback: try direct local paths
        const candidates = [
            "", "public/wiki/whats-new.md"),
            "", "../public/wiki/whats-new.md"),
            "",
        ];
        raw = readLocalFile(...candidates);
    }
    if (!raw)
        return txt("No updates available.");
    const cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - days);
    const entries = [];
    const rx = /^### (\d{4}-\d{2}-\d{2}) \| (\w+)\s*\n([\s\S]*?)(?=^### |\n## |$)/gm;
    let m;
    while ((m = rx.exec(raw)) !== null) {
        if (new Date(m[1] + "T00:00:00") >= cutoff) {
            entries.push({
                date: m[1],
                type: m[2].trim(),
                text: m[3].trim(),
            });
        }
    }
    if (entries.length === 0)
        return txt(`No new updates in the last ${days} days.`);
    const lines = [
        "# What's New in Eigen AI Terminal",
        "",
        ...entries.map((e) => `(${e.date}) [${e.type}] ${e.text}`),
        "",
        "Mention 1-2 casually at the end of the brief if relevant. Skip if nothing fresh.",
    ];
    return txt(lines.join("\n"));
});
// ─── check_updates ──────────────────────────────────────────
server.tool("check_updates", "Quick check for breaking AI developments. Hits the Eigen status endpoint — returns immediately if nothing new. If there's a breaking alert, returns the title, summary, and affected domains. Use this on a periodic schedule (every few hours) to catch breaking news between morning briefs. Only alert the user if it's relevant to their work.", {
    since: z
        .string()
        .optional()
        .describe("ISO timestamp of last check. Only returns alerts newer than this. Omit for first check."),
}, async ({ since }) => {
    const STATUS_URL = "https://terminal.clawlab.dev/api/status";
    try {
        const url = since ? `${STATUS_URL}?since=${encodeURIComponent(since)}` : STATUS_URL;
        const res = await fetch(url);
        const data = await res.json();
        if (!data.hasAlert) {
            return txt("No breaking developments. All quiet.");
        }
        const lines = [
            "# Breaking Alert",
            "",
            `**${data.title}**`,
            "",
            data.summary,
            "",
        ];
        if (data.domains?.length) {
            lines.push(`Affects: ${data.domains.join(", ")}`);
            lines.push("");
        }
        lines.push("If this is relevant to the user's work, tell them. If not, skip it.");
        lines.push(`\nUse about("${data.domains?.[0] || data.title.split(" ")[0]}") or changes("${data.since}") for full details.`);
        return txt(lines.join("\n"));
    }
    catch {
        return txt("Could not reach status endpoint. Will try again next check.");
    }
});
// ── Start ───────────────────────────────────────────────────
async function main() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("Eigen AI Terminal MCP server v1.0.0 — 12 tools available");
}
main().catch(console.error);

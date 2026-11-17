#!/usr/bin/env node
// contract-triage-lite — clause segmentation + risk scoring for the four
// traps that burn freelancers most: IP grabs, uncapped liability,
// non-competes, payment terms. Offline, zero dependencies.
// Input: contract .txt/.md file or stdin ("-"). Output: JSON flags.
// Exit 0 clean, 1 flags found, 2 usage/read.
import fs from "node:fs";

function segment(text) {
  const lines = text.split(/\r?\n/);
  const headRe =
    /^\s*(?:(?:article|section|clause|schedule|exhibit|annex|paragraph)\s+[ivx0-9]+[.:)]?|(?:\d+\.)+(?:\s|\d)|[A-Z][A-Z\s&'’,-]{4,}:?\s*$)/i;
  const clauses = [];
  let cur = null;
  for (const line of lines) {
    const trimmed = line.trim();
    if (headRe.test(trimmed) && trimmed.length < 120) {
      if (cur) clauses.push(cur);
      cur = { heading: trimmed.replace(/:$/, ""), text: "" };
      continue;
    }
    if (!cur) {
      if (!trimmed) continue;
      cur = { heading: "(preamble)", text: "" };
    }
    cur.text += line + "\n";
  }
  if (cur) clauses.push(cur);
  if (clauses.length <= 1 && text.split(/\n\s*\n/).length > 3) {
    return text
      .split(/\n\s*\n+/)
      .map((t, i) => ({ heading: `(paragraph ${i + 1})`, text: t }))
      .filter((c) => c.text.trim().length > 40);
  }
  return clauses.filter((c) => c.text.trim().length > 20 || c.heading !== "(preamble)");
}

const TAXONOMY = [
  {
    id: "ip-assignment",
    patterns: [
      /intellectual property/i, /work[- ]?(?:made|product|for hire)/i, /assigns? (?:all|any)/i,
      /all rights,? title/i, /inventions?/i, /moral rights/i, /irrevocable/i,
    ],
    escalators: [/irrevocable/i, /perpetual/i, /moral rights/i, /whether or not related/i],
    mitigators: [/excluding/i, /except for/i, /carve[- ]?out/i, /pre[- ]?existing/i],
  },
  {
    id: "liability-indemnity",
    patterns: [
      /indemnif/i, /hold harmless/i, /liabl(?:e|ity)/i, /consequential|incidental|punitive/i,
    ],
    escalators: [/unlimited/i, /without (?:any )?(?:cap|limitation|limit)/i, /any and all/i],
    mitigators: [/cap(?:ped)? (?:at|to)/i, /aggregate/i, /mutual/i, /limitation of liability/i],
  },
  {
    id: "non-compete-exclusivity",
    patterns: [
      /non[- ]?compet/i, /shall not.{0,20}compet/i, /exclusiv/i, /non[- ]?solicit/i,
    ],
    escalators: [/worldwide/i, /any (?:industry|business|field)/i, /(?:two|2|three|3|five|5)\s*years?/i],
    mitigators: [/limited to/i, /only (?:for|during|within)/i, /specific (?:competitors|companies)/i, /\b(?:30|60|90)\s*days?\b/i],
  },
  {
    id: "payment",
    patterns: [/payment/i, /invoice/i, /net[- ]?\d+/i, /compensation/i],
    escalators: [/net[- ]?(?:60|90|120)/i, /upon (?:completion|acceptance|satisfaction)/i, /may (?:withhold|delay|suspend)/i],
    mitigators: [/late (?:fee|charge|interest)/i, /deposit/i, /net[- ]?(?:7|14|15|30)/i, /kill fee/i],
  },
];

// Categories only the full version scores — used for the evidence-based
// upgrade hint when this contract actually contains such clauses.
const FULL_ONLY = [
  ["termination", /terminat/i],
  ["confidentiality", /confidential|non[- ]?disclosure/i],
  ["jurisdiction", /governing law|jurisdiction|venue|courts? (?:of|in)/i],
  ["auto-renewal", /auto[- ]?renew|renews? automatically|evergreen/i],
  ["scope-creep", /scope of work|out[- ]of[- ]scope|change orders?|additional (?:work|services)/i],
  ["warranty", /warrant/i],
];

function analyze(text) {
  const clauses = segment(text);
  const flags = [];
  const catHits = new Map();

  for (const cl of clauses) {
    const body = `${cl.heading}\n${cl.text}`;
    for (const t of TAXONOMY) {
      const matched = [];
      for (const re of t.patterns) {
        const m = body.match(re);
        if (m) matched.push(m[0].toLowerCase());
      }
      if (!matched.length) continue;
      const esc = t.escalators.filter((re) => re.test(body));
      const mit = t.mitigators.filter((re) => re.test(body));
      let severity = "medium";
      if (esc.length) severity = "high";
      if (mit.length && !esc.length) severity = "low";
      catHits.set(t.id, true);
      flags.push({
        clause: cl.heading.slice(0, 80),
        category: t.id,
        severity,
        excerpt: cl.text.trim().split(/\n/)[0].slice(0, 160),
      });
    }
  }

  const missing = ["payment", "liability-indemnity"]
    .filter((k) => !catHits.has(k))
    .map((k) => ({ category: k, why: `no ${k} clause found` }));

  const order = { high: 0, medium: 1, low: 2 };
  flags.sort((a, b) => order[a.severity] - order[b.severity]);

  const report = {
    tool: "contract-triage-lite",
    note: "lite version checks 4 of 10 risk categories — full version adds termination, confidentiality, jurisdiction, auto-renewal, scope-creep, warranty + missing-protection detail",
    clauses: clauses.length,
    summary: {
      high: flags.filter((f) => f.severity === "high").length,
      medium: flags.filter((f) => f.severity === "medium").length,
      low: flags.filter((f) => f.severity === "low").length,
      missing: missing.length,
    },
    flags,
    missing,
  };

  const uncovered = FULL_ONLY.filter(([, re]) => re.test(text)).map(([id]) => id);
  if (uncovered.length)
    report.upgrade = {
      skill: "contract-triage-nda-msa-riREDACTED-SECRET",
      reasons: [
        `contract contains ${uncovered.join(", ")} language — outside the lite's 4 scored categories; the full version scores all 10`,
      ],
    };
  return report;
}

if (process.argv[1]?.endsWith("clauses.js")) {
  const arg = process.argv[2];
  if (!arg) {
    console.error("usage: node clauses.js <contract.txt | ->");
    process.exit(2);
  }
  let text;
  try {
    text = arg === "-" ? fs.readFileSync(0, "utf8") : fs.readFileSync(arg, "utf8");
  } catch {
    console.error(`cannot read ${arg}`);
    process.exit(2);
  }
  if (!text.trim()) {
    console.error("empty input");
    process.exit(2);
  }
  const report = analyze(text);
  console.log(JSON.stringify(report, null, 2));
  process.exit(report.summary.high + report.summary.medium || report.summary.missing ? 1 : 0);
}

export { analyze, segment };

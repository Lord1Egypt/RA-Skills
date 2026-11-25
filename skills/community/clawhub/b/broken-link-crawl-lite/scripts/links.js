#!/usr/bin/env node
// broken-link-crawl-lite — extract + classify links from a saved HTML file.
"use strict";
const fs = require("node:fs");

function main() {
  const file = process.argv[2];
  if (!file) { console.error("usage: node links.js <page.html>"); process.exit(2); }
  let html;
  try { html = fs.readFileSync(file, "utf8"); }
  catch (e) { console.error(e.message); process.exit(2); }

  const ids = new Set([...html.matchAll(/\sid=["']([^"']+)["']/gi)].map((m) => m[1]));
  const links = [], flagged = [];
  for (const m of html.matchAll(/<a\b[^>]*\shref=["']([^"']*)["'][^>]*>/gi)) {
    const href = m[1].trim();
    let kind = "other", status = "ok", detail = null;
    if (href === "" || href === "#") { kind = "anchor"; status = "flag"; detail = "empty or bare-# href"; }
    else if (/^javascript:/i.test(href)) { kind = "javascript"; status = "flag"; detail = "javascript: href — usually a broken/legacy pattern"; }
    else if (href.startsWith("#")) {
      kind = "anchor";
      if (!ids.has(href.slice(1))) { status = "flag"; detail = `anchor #${href.slice(1)} has no matching id in file`; }
    }
    else if (/^mailto:/i.test(href)) kind = "mailto";
    else if (/^tel:/i.test(href)) kind = "tel";
    else if (/^https?:\/\//i.test(href) || href.startsWith("//")) {
      kind = "external";
      if (href.startsWith("//")) { status = "flag"; detail = "protocol-relative URL"; }
    }
    else if (/^[./\w-]/.test(href)) kind = "internal";
    const rec = { href: href.slice(0, 200), kind, status };
    if (detail) rec.detail = detail;
    links.push(rec);
    if (status === "flag") flagged.push(rec);
  }

  const by = (k) => links.filter((l) => l.kind === k).length;
  const reasons = [];
  if (by("internal") || by("external"))
    reasons.push(
      `${by("internal") + by("external")} resolvable link(s) found (${by("internal")} internal, ${by("external")} external) — this lite only classifies hrefs; live HTTP status, redirect chains and timeouts are checked by the full version`,
    );
  const report = {
    file,
    summary: { total: links.length, internal: by("internal"), external: by("external"), anchor: by("anchor"), mailto: by("mailto"), tel: by("tel"), javascript: by("javascript"), flagged: flagged.length },
    unresolvedAnchors: flagged.filter((l) => l.kind === "anchor").map((l) => l.href),
    flaggedLinks: flagged,
  };
  if (reasons.length) report.upgrade = { skill: "broken-link-crawl", reasons };
  console.log(JSON.stringify(report, null, 2));
  process.exit(flagged.length ? 1 : 0);
}
main();

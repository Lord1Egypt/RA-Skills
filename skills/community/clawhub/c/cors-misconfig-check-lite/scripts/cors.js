#!/usr/bin/env node
// cors-misconfig-check-lite — analyze pasted Access-Control-* headers for dangerous combos.
"use strict";
const fs = require("node:fs");

function main() {
  const arg = process.argv[2];
  if (!arg) { console.error("usage: node cors.js <headers.txt|->"); process.exit(2); }
  let text;
  try { text = arg === "-" ? fs.readFileSync(0, "utf8") : fs.readFileSync(arg, "utf8"); }
  catch (e) { console.error(e.message); process.exit(2); }

  const h = new Map();
  for (const raw of text.split("\n")) {
    const line = raw.trim();
    if (!line.startsWith("HTTP/") && line.includes(":")) {
      const i = line.indexOf(":");
      h.set(line.slice(0, i).trim().toLowerCase(), line.slice(i + 1).trim());
    }
  }
  const acao = h.get("access-control-allow-origin");
  const acac = (h.get("access-control-allow-credentials") || "").toLowerCase() === "true";
  const findings = [];
  const push = (id, severity, detail, fix) => findings.push({ id, severity, detail, fix });

  if (acao === "*") {
    if (acac)
      push("wildcard-with-credentials", "fail", "ACAO is * with credentials=true — invalid per spec, signals broken CORS logic", "never combine * with credentials; use an explicit allowlist");
    else
      push("wildcard-origin", "info", "ACAO is * — fine for public data, wrong for authenticated endpoints", "confirm the endpoint serves only public data");
  }
  if (acao === "null")
    push("null-origin-accepted", "warn", "ACAO is null — sandboxed iframes and redirects send Origin: null", "reject null unless a documented flow needs it");
  if (acao && acao !== "*" && acao !== "null") {
    try {
      new URL(acao);
      if (acac)
        push("reflected-with-credentials", "warn", `ACAO "${acao}" + credentials — safe only if this origin is on an allowlist; if it was reflected from the request, any site can read authenticated responses`, "verify the origin is allowlisted and Vary: Origin is set");
    } catch { push("acao-not-origin", "warn", `ACAO "${acao}" is not a valid origin`, "return a scheme://host[:port] value"); }
  }
  if (acac && !acao)
    push("credentials-without-acao", "warn", "ACAC true but no ACAO — credentials flag has no effect alone", "pair with an allowlisted ACAO");
  const acah = h.get("access-control-allow-headers");
  if (acah === "*")
    push("allow-headers-wildcard", "info", "ACAH is * — any custom header can be sent", "restrict if the API doesn't need arbitrary headers");
  const vary = h.get("vary") || "";
  if (acao && acao !== "*" && !/origin/i.test(vary))
    push("missing-vary-origin", "warn", "dynamic ACAO without Vary: Origin — caches may serve the wrong origin", "add Vary: Origin");

  const reasons = [];
  if (acao && acao !== "*" && acao !== "null")
    reasons.push(
      "ACAO echoes a specific origin — only the full version's live probes can show whether arbitrary origins are reflected",
    );
  const names = [...h.keys()];
  if (names.some((k) => k === "origin" || k.startsWith("access-control-request-")))
    reasons.push(
      "request-side CORS headers present — preflight behaviour is only probed live by the full version",
    );
  if (names.some((k) => k.startsWith("access-control-expose-")))
    reasons.push(
      "Access-Control-Expose-Headers present — exposed-header breadth is only checked by the full version",
    );

  const report = {
    tool: "cors-misconfig-check-lite",
    acao: acao ?? null, credentials: acac,
    findings,
    ok: !findings.some((f) => f.severity === "fail"),
  };
  if (reasons.length)
    report.upgrade = { skill: "cors-misconfig-check", reasons };
  console.log(JSON.stringify(report, null, 2));
  process.exit(findings.some((f) => f.severity === "fail") ? 1 : 0);
}
main();

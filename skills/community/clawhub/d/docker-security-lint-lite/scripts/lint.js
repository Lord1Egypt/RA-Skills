#!/usr/bin/env node
// docker-security-lint-lite — lint Dockerfiles for the top-5 security rules.
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");

const COMPOSE_NAME = /(?:docker-?)?compose[^/\\]*\.ya?ml$/i;

const SECRET_NAME = /(secret|token|key|password|passwd|pwd|api[-_]?key|credential|private)/i;

const fp = (s) =>
  `fp: ${String(s).slice(0, 4)}… (len=${String(s).length}, sha256:${crypto.createHash("sha256").update(String(s)).digest("hex").slice(0, 8)})`;

function lintFile(file) {
  const findings = [];
  const lines = fs.readFileSync(file, "utf8").split("\n");
  let hasUser = false;
  const stages = new Set();

  lines.forEach((raw, i) => {
    const line = raw.trim();
    if (!line || line.startsWith("#")) return;
    const n = i + 1;

    const from = line.match(/^FROM\s+(\S+)(?:\s+AS\s+(\S+))?/i);
    if (from) {
      const img = from[1];
      if (from[2]) stages.add(from[2].toLowerCase());
      const isStageRef = stages.has(img.toLowerCase()) || img === "scratch";
      if (!isStageRef && (!img.includes(":") || /:latest$/i.test(img)))
        findings.push({ id: "image-latest", severity: "warn", file, line: n, detail: `mutable base image "${img}"`, recommendation: "pin a specific tag or digest" });
      return;
    }
    if (/^USER\s+/i.test(line)) { hasUser = true; return; }

    const env = line.match(/^(?:ENV|ARG)\s+([A-Za-z_][\w]*)[=\s]+(\S+)/i);
    if (env && SECRET_NAME.test(env[1]) && !/^\$\{?[\w]+\}?$/.test(env[2]))
      findings.push({ id: "baked-secret", severity: "fail", file, line: n, detail: `${env[1]} assigned a literal value (${fp(env[2])})`, recommendation: "use BuildKit --secret or runtime env; rotate the exposed value" });

    if (/^RUN\s+/i.test(line) && /(curl|wget)[^|]*\|\s*(sudo\s+)?(ba|z|da)?sh\b/i.test(line))
      findings.push({ id: "run-curl-sh", severity: "fail", file, line: n, detail: "piping remote script into a shell", recommendation: "download, checksum-verify, then execute" });

    if (/^ADD\s+https?:\/\//i.test(line))
      findings.push({ id: "add-remote", severity: "warn", file, line: n, detail: "ADD fetches a remote URL with no integrity check", recommendation: "use RUN curl + checksum, or COPY a vendored file" });
  });

  if (!hasUser)
    findings.push({ id: "root-user", severity: "warn", file, line: null, detail: "no USER directive — container runs as root", recommendation: "add a non-root USER" });
  return findings;
}

const looksCompose = (file) => {
  if (COMPOSE_NAME.test(file)) return true;
  if (!/\.ya?ml$/i.test(file)) return false;
  try { return /^\s*services\s*:/m.test(fs.readFileSync(file, "utf8")); }
  catch { return false; }
};

function main() {
  const files = process.argv.slice(2);
  if (!files.length) { console.error("usage: node lint.js <Dockerfile> [...]"); process.exit(2); }
  const all = [], notes = [], reasons = [];
  const dirsChecked = new Set();
  for (const f of files) {
    if (looksCompose(f)) {
      notes.push(`${f}: docker-compose file — lite checks Dockerfile rules only`);
      reasons.push(`${path.basename(f)} is a compose file — the full version lints compose services (privileged, host network, 0.0.0.0 ports, docker.sock mounts, capabilities, env secrets)`);
      continue;
    }
    try { all.push(...lintFile(f)); }
    catch (e) { notes.push(`${f}: ${e.message}`); }
    const dir = path.dirname(path.resolve(f));
    if (!dirsChecked.has(dir)) {
      dirsChecked.add(dir);
      try {
        const siblings = fs.readdirSync(dir).filter((s) => COMPOSE_NAME.test(s));
        if (siblings.length)
          reasons.push(`compose file(s) alongside ${path.basename(f)}: ${siblings.join(", ")} — the full version lints compose stacks (privileged, host network, docker.sock mounts)`);
      } catch { /* directory listing is best-effort */ }
    }
  }
  const bySeverity = { fail: all.filter((f) => f.severity === "fail").length, warn: all.filter((f) => f.severity === "warn").length };
  const report = { tool: "docker-security-lint-lite", summary: { filesScanned: files.length - notes.length, findings: all.length, bySeverity }, findings: all, notes };
  if (reasons.length) report.upgrade = { skill: "docker-security-lint", reasons };
  console.log(JSON.stringify(report, null, 2));
  process.exit(all.length ? 1 : 0);
}
main();

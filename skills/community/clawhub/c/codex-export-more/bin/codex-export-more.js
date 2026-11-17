#!/usr/bin/env node
"use strict";

const { spawnSync } = require("child_process");
const path = require("path");

const script = path.join(__dirname, "..", "scripts", "export.py");
const candidates = [process.env.CODEX_EXPORT_PYTHON, "python3", "python"];
const python = candidates.find((c) => {
  if (!c) return false;
  const r = spawnSync(c, ["--version"], { stdio: "ignore" });
  return !r.error && r.status === 0;
}) || "python";

const result = spawnSync(python, [script, ...process.argv.slice(2)], {
  stdio: "inherit",
});

if (result.error) {
  console.error("codex-export-more: failed to launch Python: " + result.error.message);
  process.exit(1);
}
process.exit(result.status === null ? 1 : result.status);

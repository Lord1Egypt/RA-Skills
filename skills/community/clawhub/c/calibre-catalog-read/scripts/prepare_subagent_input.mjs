#!/usr/bin/env node
// Compatibility entrypoint: preparation now exports and fingerprints the real book first.
import path from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";
const pipeline = path.join(
  path.dirname(fileURLToPath(import.meta.url)),
  "run_analysis_pipeline.py",
);
const cp = spawnSync("python3", [pipeline, "prepare", ...process.argv.slice(2)], {
  stdio: "inherit",
});
if (cp.error) console.error(cp.error.message);
process.exitCode = cp.error ? 1 : (cp.status ?? 1);

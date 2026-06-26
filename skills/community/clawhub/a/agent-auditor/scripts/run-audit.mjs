#!/usr/bin/env node
// Thin wrapper for running audits from the OpenClaw skill
import { runAudit } from "@claws-shield/auditor"

const target = process.argv[2]
if (!target) {
  console.error("Usage: run-audit.mjs <path-to-source>")
  process.exit(1)
}

const report = await runAudit(target, { format: "terminal" })
console.log(JSON.stringify(report, null, 2))

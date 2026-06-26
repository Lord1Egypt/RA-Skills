#!/usr/bin/env node
// Thin wrapper for scanning skills from the OpenClaw skill
import { scanSkill } from "@claws-shield/scanner"

const skillPath = process.argv[2]
if (!skillPath) {
  console.error("Usage: run-scan.mjs <path-to-skill>")
  process.exit(1)
}

const result = await scanSkill(skillPath)
console.log(JSON.stringify(result, null, 2))

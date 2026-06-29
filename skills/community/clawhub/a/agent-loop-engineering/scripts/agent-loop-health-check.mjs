#!/usr/bin/env node
import { existsSync, readFileSync } from "node:fs"
import { resolve, join } from "node:path"

const args = process.argv.slice(2)
const workspaceArg = args.find((arg, index) => args[index - 1] === "--workspace") ?? "."
const json = args.includes("--json")
const root = resolve(workspaceArg)
const docsDir = join(root, "Docs")
const findings = []

function addFinding(finding) {
  findings.push(finding)
}

function readText(relativePath) {
  const fullPath = join(root, relativePath)
  if (!existsSync(fullPath)) {
    addFinding({
      level: "error",
      code: "missing_file",
      message: `Required CMS file is missing: ${relativePath}`,
      file: relativePath,
    })
    return ""
  }
  return readFileSync(fullPath, "utf8")
}

function checkWorkOrder() {
  const file = "Docs/WORK_ORDER.md"
  if (!existsSync(join(root, file))) return
  const text = readText(file)
  if (!text.trim()) return

  const environmentSensitive = /\b(MYWORK_[A-Z0-9_]+|VITE_[A-Z0-9_]+|Ollama|Whisper|cloud|provider|\.env|secret|token|model|device)\b/i.test(
    text,
  )
  if (!environmentSensitive) return

  const requiredSignals = [
    ["environment mode", /(local|cloud|本地|云端|environment|mode)/i],
    ["authoritative provider/config", /(provider|config|配置|\.jsonc|\.env|model)/i],
    ["feature flag", /\b([A-Z][A-Z0-9_]*=|MYWORK_[A-Z0-9_]+|VITE_[A-Z0-9_]+)\b/],
    ["waived condition", /(waived|waive|豁免|可 waived|no .* available|not available)/i],
    ["mandatory validation", /(mandatory|must|必须|须|Done 前|before `Done`|before Done)/i],
  ]

  for (const [label, pattern] of requiredSignals) {
    if (!pattern.test(text)) {
      addFinding({
        level: "warning",
        code: "work_order_missing_environment_signal",
        message: `Environment-sensitive WORK_ORDER should state ${label}.`,
        file,
      })
    }
  }
}

function checkAcceptance() {
  const file = "Docs/ACCEPTANCE.md"
  const text = readText(file)
  if (!text.trim()) return

  const idPattern = /\b([A-Z][A-Za-z0-9]*-[A-Za-z0-9]+-AC-\d{2}|P\d+[A-Za-z]*-AC-\d{2})\b/
  const seen = new Map()
  const lines = text.split(/\r?\n/)

  lines.forEach((line, index) => {
    if (!line.trim().startsWith("|")) return
    const match = line.match(idPattern)
    if (!match) return
    const id = match[1]
    const idLines = seen.get(id) ?? []
    idLines.push(index + 1)
    seen.set(id, idLines)
  })

  for (const [id, idLines] of seen.entries()) {
    if (idLines.length > 1) {
      addFinding({
        level: "error",
        code: "duplicate_acceptance_id",
        message: `${id} appears ${idLines.length} times. Keep one current AC row per active work order.`,
        file,
        line: idLines[0],
      })
    }
  }

  const pollutedPatterns = [/Agent Loop Feedback/i, /Files changed:/i, /Commands run:/i, /Required File Updates/i]
  lines.forEach((line, index) => {
    if (pollutedPatterns.some((pattern) => pattern.test(line))) {
      addFinding({
        level: "warning",
        code: "acceptance_possible_feedback_pollution",
        message: "ACCEPTANCE appears to contain raw loop feedback text.",
        file,
        line: index + 1,
      })
    }
  })
}

function parseLoopRun(line, lineNumber) {
  try {
    const value = JSON.parse(line)
    if (typeof value !== "object" || value === null || Array.isArray(value)) {
      addFinding({
        level: "error",
        code: "loop_runs_non_object",
        message: "LOOP_RUNS line must be a JSON object.",
        file: "Docs/LOOP_RUNS.jsonl",
        line: lineNumber,
      })
      return undefined
    }
    return value
  } catch (error) {
    addFinding({
      level: "error",
      code: "loop_runs_invalid_json",
      message: `Invalid JSONL line: ${error instanceof Error ? error.message : "unknown parse error"}`,
      file: "Docs/LOOP_RUNS.jsonl",
      line: lineNumber,
    })
    return undefined
  }
}

function checkLoopRuns() {
  const file = "Docs/LOOP_RUNS.jsonl"
  if (!existsSync(join(root, file))) return
  const text = readText(file)
  if (!text.trim()) return

  const runs = []
  text.split(/\r?\n/).forEach((line, index) => {
    if (!line.trim()) return
    const run = parseLoopRun(line, index + 1)
    if (!run) return
    runs.push(run)

    for (const field of ["run_id", "timestamp", "runner", "resulting_status"]) {
      if (typeof run[field] !== "string" || !run[field].trim()) {
        addFinding({
          level: "warning",
          code: "loop_runs_missing_field",
          message: `LOOP_RUNS record is missing ${field}.`,
          file,
          line: index + 1,
        })
      }
    }
  })

  const latest = runs.at(-1)
  if (!latest) return

  const latestStatus = latest.resulting_status ?? ""
  const validationRefs = Array.isArray(latest.validation_refs) ? latest.validation_refs : []
  const knownLimits = Array.isArray(latest.known_limits) ? latest.known_limits : []
  const validationText = validationRefs.join("\n").toLowerCase()

  if (latestStatus === "Done" && knownLimits.length > 0) {
    addFinding({
      level: "warning",
      code: "done_with_known_limits",
      message: "Latest loop is Done but still has known_limits. Consider Done with Risk unless limits are non-material.",
      file,
    })
  }

  if (latestStatus === "Done" && !/(pass|passed|typecheck|build succeeded|0 fail|\d+\/\d+)/i.test(validationText)) {
    addFinding({
      level: "warning",
      code: "done_without_validation_signal",
      message: "Latest loop is Done but validation_refs do not show an obvious pass/typecheck signal.",
      file,
    })
  }

  if (latestStatus === "Done" && /(blocked|fail|not recognized|missing|unavailable)/i.test(validationText)) {
    addFinding({
      level: "error",
      code: "done_with_failed_validation",
      message: "Latest loop is Done while validation_refs contain blocked/failure signals.",
      file,
    })
  }
}

function printFindings() {
  const grouped = {
    error: findings.filter((finding) => finding.level === "error"),
    warning: findings.filter((finding) => finding.level === "warning"),
    info: findings.filter((finding) => finding.level === "info"),
  }

  if (json) {
    console.log(JSON.stringify({ root, docsDir, findings, summary: {
      errors: grouped.error.length,
      warnings: grouped.warning.length,
      info: grouped.info.length,
    } }, null, 2))
    return
  }

  console.log("Agent Loop Health Check v0.1")
  console.log(`Root: ${root}`)
  console.log(`Docs: ${docsDir}`)
  console.log("")

  for (const level of ["error", "warning", "info"]) {
    if (grouped[level].length === 0) continue
    console.log(level.toUpperCase())
    for (const finding of grouped[level]) {
      const location = finding.file ? `${finding.file}${finding.line ? `:${finding.line}` : ""}` : "project"
      console.log(`- [${finding.code}] ${location} - ${finding.message}`)
    }
    console.log("")
  }

  if (grouped.error.length === 0 && grouped.warning.length === 0) {
    console.log("PASS: no Agent Loop health issues detected.")
    return
  }

  console.log(`Summary: ${grouped.error.length} error(s), ${grouped.warning.length} warning(s), ${grouped.info.length} info.`)
}

checkWorkOrder()
checkAcceptance()
checkLoopRuns()
printFindings()

process.exitCode = findings.some((finding) => finding.level === "error") ? 1 : 0

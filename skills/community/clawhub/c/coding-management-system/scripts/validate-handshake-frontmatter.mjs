#!/usr/bin/env node
/**
 * Validate CDH handshake front-matter (schema 1) on one Markdown file.
 * Contract: references/en/cross-plugin-file-contracts.md
 *
 * Usage:
 *   node validate-handshake-frontmatter.mjs --file <path> [--json]
 */

import { readFile } from 'node:fs/promises'
import { resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const REQUIRED = ['schema', 'supervisor-task-id', 'owner']

function parseArgs(argv) {
  const out = { file: undefined, json: false, help: false }
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i]
    if (arg === '--json') out.json = true
    else if (arg === '--file') out.file = argv[++i]
    else if (arg === '--help' || arg === '-h') out.help = true
    else throw new Error(`unknown argument: ${arg}`)
  }
  return out
}

function extractFence(text) {
  const match = /^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/.exec(text)
  if (match === null) return undefined
  return match[1]
}

function parseYamlLite(body) {
  const fields = Object.create(null)
  for (const rawLine of body.split(/\r?\n/)) {
    const line = rawLine.trim()
    if (line.length === 0 || line.startsWith('#')) continue
    const cut = line.indexOf(':')
    if (cut <= 0) throw new Error(`invalid front-matter line: ${rawLine}`)
    const key = line.slice(0, cut).trim()
    const value = line.slice(cut + 1).trim()
    fields[key] = value
  }
  return fields
}

/** Validate handshake front-matter against schema 1. */
export function validateHandshakeFrontMatter(text) {
  const findings = []
  const body = extractFence(text)
  if (body === undefined) {
    findings.push({ level: 'error', code: 'missing-fence', message: 'Markdown must open with a YAML --- fence' })
    return { ok: false, fields: undefined, findings }
  }
  let fields
  try {
    fields = parseYamlLite(body)
  } catch (error) {
    findings.push({ level: 'error', code: 'parse-error', message: error instanceof Error ? error.message : String(error) })
    return { ok: false, fields: undefined, findings }
  }
  for (const key of REQUIRED) {
    if (fields[key] === undefined || fields[key].length === 0) {
      findings.push({ level: 'error', code: 'missing-field', message: `required field missing: ${key}` })
    }
  }
  if (fields.schema !== undefined && fields.schema !== '1') {
    findings.push({ level: 'error', code: 'schema-mismatch', message: `schema must be 1, got ${fields.schema}` })
  }
  if (fields.owner !== undefined && fields.owner !== 'governance') {
    findings.push({ level: 'error', code: 'owner-mismatch', message: `owner must be governance, got ${fields.owner}` })
  }
  if (fields['supervisor-task-id'] !== undefined && fields['supervisor-task-id'].trim().length === 0) {
    findings.push({ level: 'error', code: 'empty-supervisor-task-id', message: 'supervisor-task-id must be non-empty' })
  }
  const unknown = Object.keys(fields).filter(key => !['schema', 'supervisor-task-id', 'owner', 'upstream'].includes(key))
  for (const key of unknown) {
    findings.push({ level: 'warning', code: 'unknown-field', message: `unknown field ignored by schema 1: ${key}` })
  }
  return {
    ok: findings.every(finding => finding.level !== 'error'),
    fields,
    findings,
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2))
  if (args.help || args.file === undefined) {
    process.stdout.write('Usage: node validate-handshake-frontmatter.mjs --file <path> [--json]\n')
    process.exitCode = args.help ? 0 : 2
    return
  }
  const text = await readFile(resolve(args.file), 'utf8')
  const result = validateHandshakeFrontMatter(text)
  if (args.json) {
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`)
  } else if (result.ok) {
    process.stdout.write(`ok schema=${result.fields?.schema} supervisor-task-id=${result.fields?.['supervisor-task-id']}\n`)
  } else {
    for (const finding of result.findings) {
      process.stderr.write(`${finding.level}: ${finding.code}: ${finding.message}\n`)
    }
  }
  process.exitCode = result.ok ? 0 : 1
}

const isDirectRun = process.argv[1] !== undefined
  && resolve(fileURLToPath(import.meta.url)) === resolve(process.argv[1])
if (isDirectRun) await main()

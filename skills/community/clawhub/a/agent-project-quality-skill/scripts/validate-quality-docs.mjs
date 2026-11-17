#!/usr/bin/env node
import fs from 'node:fs'
import process from 'node:process'
import { pathToFileURL } from 'node:url'

export const defaultConfig = {
  defectPrefix: 'DEFECT',
  improvementPrefix: 'IMPROVEMENT',
  defectType: 'defect',
  improvementType: 'improvement',
  defectTag: 'Defect',
  improvementTag: 'Improvement',
  fixedStatuses: ['fixed'],
  completedStatuses: ['completed'],
  defectRequiredFields: ['type', 'content_tag', 'status', 'severity', 'found_by', 'discovered_at', 'fixed_at', 'release_note_ready', 'affected_area'],
  improvementRequiredFields: ['type', 'content_tag', 'status', 'severity', 'proposed_by', 'started_at', 'completed_at', 'release_note_ready', 'affected_area'],
  requireReleaseCopy: true,
  releaseReadyValue: 'yes',
  evidenceHeading: 'Verification evidence',
  releaseCopyHeading: 'Release note',
  numberedSections: [],
  allowedUnnumberedH2: [],
  maxActiveRecords: null,
  maxAgentLines: null,
  maxAgentBytes: null,
  requiredBudgetPhrases: [],
  bannedCostPhrases: [],
}

function parseArgs(argv) {
  const args = {}
  for (let index = 0; index < argv.length; index += 1) {
    const key = argv[index]
    if (!key.startsWith('--')) throw new Error(`Unexpected argument: ${key}`)
    const value = argv[index + 1]
    if (!value || value.startsWith('--')) throw new Error(`Missing value for ${key}`)
    args[key.slice(2)] = value
    index += 1
  }
  return args
}

function parseFrontmatter(text) {
  const match = text.match(/^---\r?\n([\s\S]*?)\r?\n---/)
  if (!match) return null
  return Object.fromEntries(match[1].split(/\r?\n/).filter(Boolean).map((line) => {
    const split = line.indexOf(':')
    return split < 0 ? [line.trim(), ''] : [line.slice(0, split).trim(), line.slice(split + 1).trim()]
  }))
}

function maskFences(text) {
  return text.replace(/```[\s\S]*?```/g, (block) => block.replace(/[^\r\n]/g, ' '))
}

function headings(text) {
  return [...maskFences(text).matchAll(/^(#{1,6})\s+(.+)$/gm)].map((match) => ({ level: match[1].length, title: match[2].trim() }))
}

function parseYamlBlock(body) {
  const match = body.match(/```yaml\r?\n([\s\S]*?)\r?\n```/)
  if (!match) return null
  return Object.fromEntries(match[1].split(/\r?\n/).filter(Boolean).map((line) => {
    const split = line.indexOf(':')
    return [line.slice(0, split).trim(), line.slice(split + 1).trim()]
  }))
}

function exactTimestamp(value) {
  const match = value?.match(/^(\d{4}-\d{2}-\d{2})[ T](\d{2}:\d{2})/)
  return match ? `${match[1]} ${match[2]}` : ''
}

export function validateQualityDocs({ specText, logText, archiveTexts = [], agentsText = '', workflowText = '', config = {} }) {
  const settings = { ...defaultConfig, ...config }
  const diagnostics = []
  const specMeta = parseFrontmatter(specText)
  const logMeta = parseFrontmatter(logText)
  if (!specMeta) diagnostics.push('Specification is missing frontmatter.')
  if (!logMeta) diagnostics.push('Log is missing frontmatter.')

  for (const [label, text] of [['Specification', specText], ['Log', logText]]) {
    const list = headings(text)
    if (list.filter((item) => item.level === 1).length !== 1) diagnostics.push(`${label} must contain exactly one H1.`)
    for (let index = 1; index < list.length; index += 1) {
      if (list[index].level > list[index - 1].level + 1) diagnostics.push(`${label} has a heading-level jump at "${list[index].title}".`)
    }
  }

  if (settings.numberedSections.length) {
    const h2Titles = headings(specText).filter((item) => item.level === 2).map((item) => item.title)
    const actual = h2Titles.map((title) => title.match(/^(\d+)\./)?.[1]).filter(Boolean).map(Number)
    if (JSON.stringify(actual) !== JSON.stringify(settings.numberedSections)) diagnostics.push(`Specification numbered H2 sections do not match configuration: ${actual.join(', ')}.`)
    if (settings.allowedUnnumberedH2.length) {
      const unexpected = h2Titles.filter((title) => !/^\d+\./.test(title) && !settings.allowedUnnumberedH2.includes(title))
      if (unexpected.length) diagnostics.push(`Specification has unapproved unnumbered H2 sections: ${unexpected.join(', ')}.`)
    }
  }

  const idPattern = `(?:${settings.defectPrefix}|${settings.improvementPrefix})-[A-Z0-9_-]+`
  const summarySection = logText.match(/## Status Index\s+([\s\S]*?)(?=\n---)/i)
  if (!summarySection) diagnostics.push('Log is missing the Status Index section.')
  const summaryRows = summarySection ? [...summarySection[1].matchAll(new RegExp(`^\\|\\s*(${idPattern})\\s*\\|\\s*([^|]+)\\|`, 'gm'))] : []
  const summaryIds = summaryRows.map((row) => row[1])
  if (new Set(summaryIds).size !== summaryIds.length) diagnostics.push('Status Index contains duplicate identifiers.')
  if (settings.maxActiveRecords !== null && summaryIds.length > settings.maxActiveRecords) diagnostics.push(`Active log exceeds the configured limit of ${settings.maxActiveRecords} records.`)

  const detailPattern = new RegExp(`^## (${idPattern}):[^\\r\\n]+\\r?\\n([\\s\\S]*?)(?=^---\\s*$|^## Templates|(?![\\s\\S]))`, 'gm')
  const details = [...logText.matchAll(detailPattern)]
  const detailIds = details.map((record) => record[1])
  const archiveDetails = archiveTexts.flatMap((text) => [...text.matchAll(detailPattern)])
  const archiveIds = archiveDetails.map((record) => record[1])
  const allIds = [...detailIds, ...archiveIds]
  if (new Set(allIds).size !== allIds.length) diagnostics.push('Active and archived records contain duplicate identifiers.')
  const missingDetails = summaryIds.filter((id) => !detailIds.includes(id))
  const missingSummary = detailIds.filter((id) => !summaryIds.includes(id))
  if (missingDetails.length) diagnostics.push(`Index identifiers missing details: ${missingDetails.join(', ')}.`)
  if (missingSummary.length) diagnostics.push(`Detailed identifiers missing from index: ${missingSummary.join(', ')}.`)

  let newestCompletion = ''
  for (const record of [...details, ...archiveDetails]) {
    const id = record[1]
    const body = record[2]
    const fields = parseYamlBlock(body)
    if (!fields) {
      diagnostics.push(`${id} is missing a YAML metadata block.`)
      continue
    }
    const isDefect = id.startsWith(`${settings.defectPrefix}-`)
    const required = isDefect ? settings.defectRequiredFields : settings.improvementRequiredFields
    for (const field of required) if (!(field in fields)) diagnostics.push(`${id} is missing required field ${field}.`)
    const expectedType = isDefect ? settings.defectType : settings.improvementType
    const expectedTag = isDefect ? settings.defectTag : settings.improvementTag
    if (fields.type !== expectedType) diagnostics.push(`${id} type must be ${expectedType}.`)
    if (fields.content_tag !== expectedTag) diagnostics.push(`${id} content_tag must be ${expectedTag}.`)
    const indexRow = detailIds.includes(id) ? summaryRows.find((row) => row[1] === id) : undefined
    if (indexRow && indexRow[2].trim() !== expectedTag) diagnostics.push(`${id} index label does not match its record type.`)
    const completed = (isDefect ? settings.fixedStatuses : settings.completedStatuses).includes(fields.status)
    const endField = isDefect ? 'fixed_at' : 'completed_at'
    if (completed && !fields[endField]) diagnostics.push(`${id} is complete but ${endField} is empty.`)
    if (completed && !body.includes(`**${settings.evidenceHeading}`)) diagnostics.push(`${id} is complete but verification evidence is missing.`)
    if (settings.requireReleaseCopy && fields.release_note_ready === settings.releaseReadyValue && !body.includes(`**${settings.releaseCopyHeading}`)) diagnostics.push(`${id} is release-ready but release copy is missing.`)
    const timestamp = exactTimestamp(fields[endField])
    if (detailIds.includes(id) && timestamp > newestCompletion) newestCompletion = timestamp
  }

  const updated = exactTimestamp(logMeta?.last_updated)
  if (newestCompletion && (!updated || updated < newestCompletion)) diagnostics.push(`Log last_updated is older than the newest completed record (${newestCompletion}).`)

  if (agentsText) {
    const lineCount = agentsText.split(/\r?\n/).length
    if (settings.maxAgentLines !== null && lineCount > settings.maxAgentLines) diagnostics.push(`Agent entrypoint exceeds ${settings.maxAgentLines} lines.`)
    if (settings.maxAgentBytes !== null && Buffer.byteLength(agentsText, 'utf8') > settings.maxAgentBytes) diagnostics.push(`Agent entrypoint exceeds ${settings.maxAgentBytes} bytes.`)
    for (const phrase of settings.requiredBudgetPhrases) if (!agentsText.includes(phrase)) diagnostics.push(`Agent entrypoint is missing required budget phrase: ${phrase}`)
  }
  const governanceText = [agentsText, specText, workflowText].filter(Boolean).join('\n')
  for (const phrase of settings.bannedCostPhrases) if (governanceText.includes(phrase)) diagnostics.push(`Governance documents contain banned cost rule: ${phrase}`)
  return diagnostics
}

export function runCli(argv = process.argv.slice(2)) {
  let args
  try {
    args = parseArgs(argv)
  } catch (error) {
    console.error(error.message)
    return 2
  }
  if (!args.spec || !args.log) {
    console.error('Usage: node validate-quality-docs.mjs --spec <file> --log <file> [--archives <file1,file2>] [--agents <file>] [--workflow <file>] [--config <json>]')
    return 2
  }
  try {
    const config = args.config ? JSON.parse(fs.readFileSync(args.config, 'utf8')) : {}
    const archiveTexts = args.archives ? args.archives.split(',').filter(Boolean).map((file) => fs.readFileSync(file, 'utf8')) : []
    const agentsText = args.agents ? fs.readFileSync(args.agents, 'utf8') : ''
    const workflowText = args.workflow ? fs.readFileSync(args.workflow, 'utf8') : ''
    const diagnostics = validateQualityDocs({ specText: fs.readFileSync(args.spec, 'utf8'), logText: fs.readFileSync(args.log, 'utf8'), archiveTexts, agentsText, workflowText, config })
    if (diagnostics.length) {
      console.error('QUALITY DOCS CHECK FAILED')
      diagnostics.forEach((item) => console.error(`- ${item}`))
      return 1
    }
    console.log('QUALITY DOCS CHECK OK')
    return 0
  } catch (error) {
    console.error(`Unable to validate documents: ${error.message}`)
    return 2
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) process.exitCode = runCli()

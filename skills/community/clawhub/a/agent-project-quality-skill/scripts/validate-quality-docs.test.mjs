import assert from 'node:assert/strict'
import { spawnSync } from 'node:child_process'
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import test from 'node:test'
import { fileURLToPath } from 'node:url'
import { validateQualityDocs } from './validate-quality-docs.mjs'

const config = {
  numberedSections: [0, 1],
  allowedUnnumberedH2: ['Index'],
  fixedStatuses: ['fixed'],
  completedStatuses: ['completed'],
}

const validSpec = `---
document_type: technical-specification
last_updated: 2099-01-02 10:00 +00:00
---
# Example Specification
## 0. Mandatory Rules
## Index
### Reading Routes
## 1. Architecture
`

const validLog = `---
document_type: quality-log
last_updated: 2099-01-02 10:00 +00:00
---
# Quality Log
## Status Index
| ID | Content label | Status | Severity | Summary |
|---|---|---|---|---|
| DEFECT-ALPHA-001 | Defect | fixed | medium | Example defect |
| IMPROVEMENT-BETA-001 | Improvement | completed | low | Example improvement |
---
## DEFECT-ALPHA-001: Example defect

\`\`\`yaml
type: defect
content_tag: Defect
status: fixed
severity: medium
found_by: reviewer
discovered_at: 2099-01-01 09:00 +00:00
fixed_at: 2099-01-01 10:00 +00:00
release_note_ready: yes
affected_area: example module
\`\`\`

**Verification evidence:** Focused test passed.

**Release note:** Corrected an example behavior.

---
## IMPROVEMENT-BETA-001: Example improvement

\`\`\`yaml
type: improvement
content_tag: Improvement
status: completed
severity: low
proposed_by: reviewer
started_at: 2099-01-01 09:00 +00:00
completed_at: 2099-01-02 10:00 +00:00
release_note_ready: no
affected_area: documentation
\`\`\`

**Verification evidence:** Validation passed.

---
## Templates
`

const validArchive = `---
document_type: quality-log-archive
period: 2099-Q1
---
# Quality Log Archive
## IMPROVEMENT-GAMMA-001: Archived improvement

\`\`\`yaml
type: improvement
content_tag: Improvement
status: completed
severity: low
proposed_by: reviewer
started_at: 2099-01-01 08:00 +00:00
completed_at: 2099-01-01 09:00 +00:00
release_note_ready: no
affected_area: documentation
\`\`\`

**Verification evidence:** Archived validation passed.
`

test('accepts a valid specification and log', () => {
  assert.deepEqual(validateQualityDocs({ specText: validSpec, logText: validLog, archiveTexts: [validArchive], config }), [])
})

test('detects a heading jump', () => {
  const result = validateQualityDocs({ specText: validSpec.replace('### Reading Routes', '#### Reading Routes'), logText: validLog, config })
  assert.ok(result.some((item) => item.includes('heading-level jump')))
})

test('detects duplicate and missing identifiers', () => {
  const changed = validLog.replace('| IMPROVEMENT-BETA-001 | Improvement | completed | low | Example improvement |', '| DEFECT-ALPHA-001 | Defect | fixed | medium | Duplicate |')
  const result = validateQualityDocs({ specText: validSpec, logText: changed, config })
  assert.ok(result.some((item) => item.includes('duplicate identifiers')))
  assert.ok(result.some((item) => item.includes('missing from index')))
})

test('detects type and label mismatch', () => {
  const changed = validLog.replace('content_tag: Defect', 'content_tag: Improvement')
  const result = validateQualityDocs({ specText: validSpec, logText: changed, config })
  assert.ok(result.some((item) => item.includes('content_tag must be Defect')))
})

test('detects missing required fields and evidence', () => {
  const changed = validLog.replace('found_by: reviewer\n', '').replace('**Verification evidence:** Focused test passed.\n', '')
  const result = validateQualityDocs({ specText: validSpec, logText: changed, config })
  assert.ok(result.some((item) => item.includes('missing required field found_by')))
  assert.ok(result.some((item) => item.includes('verification evidence is missing')))
})

test('detects missing release copy', () => {
  const changed = validLog.replace('**Release note:** Corrected an example behavior.\n', '')
  const result = validateQualityDocs({ specText: validSpec, logText: changed, config })
  assert.ok(result.some((item) => item.includes('release copy is missing')))
})

test('detects a stale log update time', () => {
  const changed = validLog.replace('last_updated: 2099-01-02 10:00 +00:00', 'last_updated: 2099-01-01 08:00 +00:00')
  const result = validateQualityDocs({ specText: validSpec, logText: changed, config })
  assert.ok(result.some((item) => item.includes('last_updated is older')))
})

test('detects identifiers duplicated between active and archived logs', () => {
  const duplicatedArchive = validArchive.replaceAll('IMPROVEMENT-GAMMA-001', 'IMPROVEMENT-BETA-001')
  const result = validateQualityDocs({ specText: validSpec, logText: validLog, archiveTexts: [duplicatedArchive], config })
  assert.ok(result.some((item) => item.includes('duplicate identifiers')))
})

test('enforces configured active-log and context budgets', () => {
  const result = validateQualityDocs({
    specText: validSpec,
    logText: validLog,
    agentsText: 'default entrypoint',
    workflowText: 'Every commit requires full validation.',
    config: {
      ...config,
      maxActiveRecords: 1,
      maxAgentLines: 1,
      requiredBudgetPhrases: ['targeted reading'],
      bannedCostPhrases: ['Every commit requires full validation.'],
    },
  })
  assert.ok(result.some((item) => item.includes('Active log exceeds')))
  assert.ok(result.some((item) => item.includes('missing required budget phrase')))
  assert.ok(result.some((item) => item.includes('banned cost rule')))
})

test('runs through the explicit-path CLI in an isolated directory', () => {
  const directory = mkdtempSync(join(tmpdir(), 'quality-docs-'))
  try {
    const specPath = join(directory, 'spec.md')
    const logPath = join(directory, 'log.md')
    const configPath = join(directory, 'config.json')
    writeFileSync(specPath, validSpec)
    writeFileSync(logPath, validLog)
    writeFileSync(configPath, JSON.stringify(config))
    const scriptPath = fileURLToPath(new URL('./validate-quality-docs.mjs', import.meta.url))
    const result = spawnSync(process.execPath, [scriptPath, '--spec', specPath, '--log', logPath, '--config', configPath], { encoding: 'utf8' })
    assert.equal(result.status, 0, result.stderr)
    assert.match(result.stdout, /QUALITY DOCS CHECK OK/)
  } finally {
    rmSync(directory, { recursive: true, force: true })
  }
})

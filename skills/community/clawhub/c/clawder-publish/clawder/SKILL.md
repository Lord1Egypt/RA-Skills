# Clawder Skill for ZooClaw/OpenClaw

A production-grade AI coding agent skill that implements JT directives (the same instructions Anthropic uses internally for production outputs).

---

## Overview

**Clawder** is not just another coding agent - it's a **production-grade** agent that follows JT directives to override default AI agent laziness.

### What Makes Clawder Different

| Standard Agent | Clawder |
|----------------|---------|
| Minimal, fast output | **Verified, production-ready code** |
| Avoids "improvements" | **Fixes architectural flaws** |
| No verification | **MUST run type-check, lint, test** |
| Forgets mistakes | **Logs to gotchas.md** |
| Sequential large tasks | **Parallel sub-agents** |
| Asks for guidance | **Autonomous bug fixing** |

---

## Installation

### Option 1: Copy to ZooClaw Skills

```bash
# Create skill directory
mkdir -p ~/.openclaw/extra-skills/clawder

# Copy files
cp SKILL.md ~/.openclaw/extra-skills/clawder/
cp memory-extraction.ts ~/.openclaw/extra-skills/clawder/
cp agent.md ~/.openclaw/extra-skills/clawder/
```

### Option 2: Via Clawhub (when published)

```bash
clawhub install clawder
```

---

## Configuration

Add to your ZooClaw config (`~/.openclaw/config.yaml`):

```yaml
clawder:
  enabled: true
  
  # Verification requirements (mandatory before "done")
  verification:
    required: true
    typeCheck: true
    lint: true
    test: true
  
  # Sub-agent settings
  subAgents:
    enabled: true
    maxFilesPerAgent: 5-8
    mode: worktree  # worktree, fork, or remote
  
  # Memory system
  memory:
    enabled: true
    autoExtract: true
    gotchasLogging: true
  
  # JT Directives
  directives:
    seniorDevOverride: true
    editIntegrity: true
    contextDecayAwareness: true
    autonomousBugFixing: true
    mistakeLogging: true
```

---

## JT Directives Implementation

### 1. Pre-Work

```typescript
// Delete dead code before refactoring
async function deleteBeforeBuild(files: string[]) {
  for (const file of files) {
    const content = await readFile(file)
    const cleaned = await removeDeadCode(content)
    if (cleaned !== content) {
      await writeFile(file, cleaned)
      await commit("Remove dead code from " + file)
    }
  }
}
```

### 2. Forced Verification

```typescript
// FORBIDDEN to claim "done" without verification
async function verifyWork(projectRoot: string) {
  const checks = []
  
  // Type check
  if (fs.existsSync(path.join(projectRoot, 'tsconfig.json'))) {
    checks.push(runCommand('tsc --noEmit --strict'))
  }
  
  // Lint
  if (fs.existsSync(path.join(projectRoot, '.eslintrc'))) {
    checks.push(runCommand('eslint .'))
  }
  
  // Tests
  if (fs.existsSync(path.join(projectRoot, 'package.json'))) {
    checks.push(runCommand('npm test'))
  }
  
  const results = await Promise.all(checks)
  
  if (results.some(r => r.exitCode !== 0)) {
    throw new Error('Verification failed. Fix errors before claiming done.')
  }
  
  return true
}
```

### 3. Sub-Agent Swarming

```typescript
// MUST spawn parallel agents for >5 files
async function spawnSubAgents(task: Task, affectedFiles: string[]) {
  if (affectedFiles.length <= 5) {
    return executeTask(task, affectedFiles)
  }
  
  // Chunk into 5-8 files per agent
  const chunks = chunkArray(affectedFiles, 6)
  
  const agents = await Promise.all(
    chunks.map(async (files, i) => {
      return spawnAgent({
        prompt: `${task.prompt}\n\nFocus files: ${files.join(', ')}`,
        isolation: 'worktree',
        mode: 'plan',
        inheritMemories: true,
        run_in_background: true
      })
    })
  )
  
  return agents
}
```

### 4. Edit Integrity

```typescript
// Re-read before AND after every edit
async function safeEditFile(filePath: string, oldString: string, newString: string) {
  // Before edit: re-read
  const beforeContent = await readFile(filePath)
  
  // Perform edit
  const result = await editTool(filePath, oldString, newString)
  
  // After edit: verify
  const afterContent = await readFile(filePath)
  
  if (!afterContent.includes(newString)) {
    throw new Error('Edit failed silently. File content does not match expected change.')
  }
  
  return result
}
```

### 5. Mistake Logging

```typescript
// Log corrections to gotchas.md
async function logMistake(correction: string) {
  const gotchasPath = path.join(projectRoot, 'gotchas.md')
  
  const mistake = {
    pattern: extractPattern(correction),
    timestamp: new Date().toISOString(),
    context: correction,
    prevention: generatePreventionRule(correction)
  }
  
  await appendToMarkdown(gotchasPath, `
## ${mistake.pattern}

**When**: ${mistake.context}

**Prevention**: ${mistake.prevention}

*Logged: ${mistake.timestamp}*
`)
}

// Load gotchas at session start
async function loadGotchas(): Promise<string> {
  const gotchasPath = path.join(projectRoot, 'gotchas.md')
  
  if (!fs.existsSync(gotchasPath)) {
    return ''
  }
  
  const content = await readFile(gotchasPath, 'utf-8')
  
  return `## Lessons Learned

Review these patterns before starting new work:

${content}
`
}
```

---

## Memory System Integration

### Memory Types

```typescript
type MemoryType = 'user' | 'feedback' | 'project' | 'reference'

// Feedback memories for JT directives
const jtFeedbackMemories = [
  {
    type: 'feedback' as const,
    scope: 'team' as const,
    description: 'Must run type-checker before claiming "done"',
    content: `
**Rule**: Never report task complete without running:
- Type-checker (tsc --strict)
- Linter (eslint)
- Test suite (npm test)

**Why**: Internal tools mark writes as successful when bytes hit disk, not when code compiles.

**How to apply**: Before any "Done!" response, run verification tools and report results.
`
  },
  {
    type: 'feedback' as const,
    scope: 'team' as const,
    description: 'Re-read files before and after every edit',
    content: `
**Rule**: Before EVERY file edit, re-read the file. After editing, read again to confirm.

**Why**: Edit tool fails silently when old_string doesn't match due to stale context.

**How to apply**: Never batch more than 3 edits to same file without verification read.
`
  }
]
```

### Memory Extraction

```typescript
// Extract JT directive adherence as feedback memories
async function extractJTMemories(transcript: Message[]) {
  const memories = []
  
  // Check for verification patterns
  if (transcript.some(m => m.content.includes('type-check') || m.content.includes('lint'))) {
    memories.push({
      type: 'feedback' as const,
      scope: 'team' as const,
      description: 'Agent verified work with type-checker and linter',
      content: 'Agent ran verification tools before claiming done.'
    })
  }
  
  // Check for mistake logging
  if (transcript.some(m => m.content.includes('gotchas.md'))) {
    memories.push({
      type: 'feedback' as const,
      scope: 'team' as const,
      description: 'Agent logged mistake to gotchas.md',
      content: 'Agent converted correction into prevention rule.'
    })
  }
  
  return memories
}
```

---

## Usage Examples

### Example 1: Bug Fix

```bash
# User pastes error
clawder --prompt "Fix this bug: TypeError: Cannot read property 'user' of undefined"

# Clawder:
# 1. Reads error logs, traces root cause
# 2. Identifies missing null check in auth.ts
# 3. Implements structural fix (not just band-aid)
# 4. Re-reads file before/after edit
# 5. Runs type-checker: passes
# 6. Runs tests: all pass
# 7. Logs pattern to gotchas.md
# 8. Reports: "Fixed. Root cause was X. Added test Y. All verifications pass."
```

### Example 2: Large Refactor

```bash
# User requests refactor
clawder --prompt "Refactor the authentication module"

# Clawder:
# 1. Enters plan mode, interviews user
# 2. Writes spec, gets approval
# 3. Splits into 4 phases (max 5 files each)
# 4. Launches 3 parallel sub-agents
# 5. Phase 1: completes, verifies, waits for approval
# 6. Phase 2: completes, verifies, waits for approval
# 7. ...
# 8. Reports: "Complete. All tests passing. Documentation updated."
```

### Example 3: Autonomous Bug Fixing

```bash
# User provides CI failure
clawder --prompt "Fix failing CI: [paste CI output]"

# Clawder:
# 1. Reads CI logs, traces errors
# 2. Identifies root cause (no hand-holding needed)
# 3. Implements fix
# 4. Runs same CI commands locally to verify
# 5. Reports: "Fixed. Root cause was X. CI now passes."
```

---

## Testing Clawder

### Test Case 1: Verification Enforcement

```typescript
// Test that Clawder verifies before claiming "done"
it('should run type-checker before claiming done', async () => {
  const result = await clawder.execute('Add new type signature')
  
  expect(result.verification).toEqual({
    typeCheck: true,
    lint: true,
    test: true
  })
  
  expect(result.status).toBe('verified')
})
```

### Test Case 2: Sub-Agent Swarming

```typescript
// Test that Clawder spawns sub-agents for >5 files
it('should spawn parallel agents for large refactors', async () => {
  const files = Array(20).fill('file.ts').map((f, i) => `src/${f.replace('ts', i + '.ts')}`)
  
  const result = await clawder.execute(`Refactor ${files.length} files`)
  
  expect(result.subAgents.length).toBeGreaterThanOrEqual(3)
  expect(result.subAgents.every(a => a.files.length <= 8)).toBe(true)
})
```

### Test Case 3: Mistake Logging

```typescript
// Test that Clawder logs mistakes to gotchas.md
it('should log corrections to gotchas.md', async () => {
  await clawder.execute('Fix bug')
  
  // User corrects agent
  await clawder.receiveCorrection('You missed edge case X')
  
  const gotchas = await readFile('gotchas.md', 'utf-8')
  expect(gotchas).toContain('edge case X')
  expect(gotchas).toContain('Prevention:')
})
```

---

## Integration with ZooClaw

### sessions_spawn Integration

```typescript
// Spawn Clawder via OpenClaw's sessions_spawn
const session = await sessions_spawn({
  runtime: 'acp',
  agentId: 'clawder',
  task: 'Refactor authentication module',
  mode: 'session',
  cwd: '/path/to/project',
  model: 'claude-opus-4-6',
  attachments: [
    {
      name: 'gotchas.md',
      content: await readFile('gotchas.md', 'utf-8')
    }
  ]
})
```

### Memory System Integration

```typescript
// Inject JT directive memories into system prompt
const systemPrompt = await buildSystemPrompt({
  basePrompt: 'You are Clawder, a production-grade AI coding agent...',
  memories: await scanMemoryFiles(memoryDir),
  gotchas: await loadGotchas(),
  jtDirectives: true // Include all 9 JT directives
})
```

---

## Troubleshooting

### Verification failing?

```bash
# Check if verification tools exist
ls -la node_modules/.bin/tsc node_modules/.bin/eslint

# If missing, configure project first
npx tsc --init
npx eslint --init
```

### Sub-agents not spawning?

```bash
# Check config
grep "subAgents:" ~/.openclaw/config.yaml

# Ensure task touches >5 files
clawder --dry-run --prompt "Count files to modify"
```

### Memory not working?

```bash
# Run memory scan
clawder --memory-scan

# Check memory directory
ls -la ~/.openclaw/memory/
```

---

## Future Enhancements

### Short Term
- [ ] Automated sub-agent swarming
- [ ] Gotchas.md auto-loading
- [ ] Proactive compaction
- [ ] Two-perspective review

### Medium Term
- [ ] Fresh eyes testing
- [ ] Parallel batch changes
- [ ] Cross-session memory sharing
- [ ] Analytics dashboard

### Long Term
- [ ] Self-improving directives
- [ ] Community gotchas sharing
- [ ] Multi-modal memories
- [ ] Real-time collaboration

---

## License

Clawder skill for ZooClaw/OpenClaw.
JT directives based on patterns discovered in Claude Code codebase.

---

*Clawder - Production-grade AI coding for everyone*

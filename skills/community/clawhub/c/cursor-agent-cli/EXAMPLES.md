# Cursor CLI Examples

## Example 1: Interactive Refactoring

```bash
agent "refactor the authentication module to use JWT tokens"
```

**What happens:**
1. Agent analyzes current auth code
2. Proposes refactoring plan
3. Shows file changes
4. Asks for approval
5. Executes changes
6. Runs validation

## Example 2: Bug Fix

```bash
agent -p "find and fix the memory leak in server.js" --force
```

**Non-interactive, auto-approved bug fixing.**

## Example 3: Code Review

```bash
# Review uncommitted changes
git diff | agent -p "review these changes for security issues"

# Review specific file
agent "review api/auth.js for potential vulnerabilities"
```

## Example 4: Test Generation

```bash
agent "generate comprehensive unit tests for src/utils/*.js with 90% coverage"
```

## Example 5: Documentation

```bash
agent "add JSDoc comments to all exported functions in this directory"
```

## Example 6: Performance Optimization

```bash
agent --plan "analyze database queries and suggest optimizations"
```

**Plan mode first to review approach before making changes.**

## Example 7: Feature Development

```bash
agent -c "implement user profile editing feature with validation and tests"
```

**Cloud mode - runs in background, check back later.**

## Example 8: Migration

```bash
agent "migrate from Express to Fastify maintaining all functionality"
```

## Example 9: CI/CD Integration

```bash
#!/bin/bash
# .github/workflows/ai-review.sh

agent -p "review changed files for security and performance issues" \
  --output-format json \
  --trust \
  --workspace $GITHUB_WORKSPACE \
  > ai-review.json

# Parse results
jq '.issues' ai-review.json
```

## Example 10: Multiple Models

```bash
# Use GPT-5 for complex refactoring
agent --model gpt-5.2 "refactor monolith into microservices"

# Use Sonnet-4 for careful analysis
agent --model sonnet-4-thinking "analyze potential race conditions"
```

## Example 11: Workspace-specific

```bash
# Work on specific project
agent --workspace /path/to/project "fix build errors"
```

## Example 12: Git Worktree

```bash
# Create isolated worktree for feature
agent -w feature-auth --worktree-base main "implement OAuth2 authentication"

# Work continues in ~/.cursor/worktrees/myrepo/feature-auth
```

## Example 13: Session Management

```bash
# Create new session
agent create-chat

# List all sessions
agent ls

# Resume specific session
agent --resume="chat-abc123"

# Continue latest
agent --continue
```

## Example 14: Output Formats

```bash
# JSON for parsing
agent -p "list all API endpoints" --output-format json > endpoints.json

# Streaming JSON for real-time processing
agent -p "analyze code" --output-format stream-json --stream-partial-output
```

## Example 15: Custom Headers

```bash
# Add authentication
agent -H "Authorization: Bearer token123" \
      -H "X-Project-ID: proj-456" \
      "deploy to staging"
```

---

## OpenClaw Integration Examples

### Example A: Call from OpenClaw

```javascript
// Interactive session (requires PTY)
exec({ 
  command: "agent 'refactor auth module'",
  pty: true 
})

// Non-interactive
exec({ 
  command: "agent -p 'analyze code structure' --output-format json"
})
```

### Example B: Parse JSON Output

```javascript
const result = await exec({
  command: "agent -p 'list functions in api.js' --output-format json"
});

const data = JSON.parse(result);
console.log(data.functions);
```

### Example C: Automated Workflow

```javascript
// Step 1: Plan
await exec({
  command: "agent --plan 'refactor database layer' > plan.txt"
});

// Step 2: Review plan
const plan = await read({ path: "plan.txt" });
console.log("Plan:", plan);

// Step 3: Execute if approved
await exec({
  command: "agent -p 'execute the refactoring plan' --force"
});
```

---

**Tip**: Always use `--plan` mode first for complex changes to review the approach before execution!

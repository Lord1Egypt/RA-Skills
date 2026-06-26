# Sequential Pipeline — `claude -p` Loops

The simplest loop: chain `claude -p` calls in a bash script. Each call is a focused step, exits when done, then the next step begins.

## Basic Example

```bash
#!/bin/bash
set -e  # Exit on first failure

# Step 1: Implement
claude -p "Read docs/spec.md. Implement OAuth2 login in src/auth/. Write tests first (TDD)."

# Step 2: Clean up
claude -p "Review changes. Remove unnecessary test assertions and overly defensive checks. Keep business logic tests. Run tests after cleanup."

# Step 3: Verify
claude -p "Run full build, lint, type check, test suite. Fix any failures."

# Step 4: Commit
claude -p "Create conventional commit for all changes. Message: 'feat: add OAuth2 login'"
```

## Key Design

1. **Each step is isolated** — Fresh context window, no bleed-through
2. **Order matters** — Sequential execution
3. **Negative instructions are risky** — Say "don't do X" and the model becomes hesitant about everything. Use a separate cleanup step instead.
4. **`set -e` stops on failure** — Pipeline halts at first error

## With Model Routing

```bash
# Research with strong model
claude -p --model opus "Analyze the codebase architecture and write a plan..."

# Implement with capable model
claude -p "Implement according to the plan..."

# Review with strong model
claude -p --model opus "Review for security issues, race conditions, edge cases..."
```

## Context Bridge: SHARED_TASK_NOTES.md

Since each `claude -p` call is fresh, use a file to track progress:

```markdown
# Task: Add authentication

## Progress
- [x] Analyzed architecture
- [x] Wrote implementation plan
- [ ] Implemented OAuth2 flow
- [ ] Added tests
- [ ] Cleaned up
- [ ] Verified

## Next Steps
- Focus on OAuth2 integration
- Mock auth service for tests
- Use existing token validation logic
```

Each step reads this file and updates it:

```bash
claude -p "Read SHARED_TASK_NOTES.md. Work on the current 'Next Steps'. Update the progress section when done."
```

## Environment Context

Pass context via files instead of prompt length:

```bash
# Create context file
cat > .claude-context.md << EOF
Priority areas:
- Auth module (highest)
- Rate limiting (medium)
- Caching (lower)
EOF

# Pass reference to file
claude -p "Read .claude-context.md for priorities. Work through them in order."

# Clean up
rm .claude-context.md
```

## Tool Restrictions

Limit what Claude can do in certain steps:

```bash
# Read-only analysis
claude -p --allowedTools "Read,Grep,Glob" "Audit this codebase for security vulnerabilities..."

# Implementation only
claude -p --allowedTools "Read,Write,Edit,Bash" "Implement the fixes from audit.md..."
```

## Error Handling

When a step fails, capture context for the next attempt:

```bash
#!/bin/bash

# Try implementation
if ! claude -p "Implement feature X..."; then
  # Capture failure context
  echo "Implementation failed. Log output:" > .error-context.md
  git diff >> .error-context.md
  
  # Next attempt includes context
  claude -p "Previous implementation failed (see .error-context.md). Try a different approach..."
fi
```

## When NOT to Use Sequential

- Too many steps (becomes hard to track)
- Steps need human judgment (add review gates)
- Parallel work is critical (use Parallel Agents instead)
- Merge conflicts likely (use DAG Orchestration instead)

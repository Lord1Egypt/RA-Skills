# Context Optimization Patterns

## Summarization Patterns

### Task Completion Pattern

**Before (verbose):**
```
- User asked for a script to process CSV files
- I wrote process_csv.py with pandas
- Had an issue with encoding, fixed by specifying utf-8
- Added error handling for missing columns
- User tested, approved, deployed to production
```

**After (compact):**
```
## Task: CSV Processing Script
- Built process_csv.py (pandas, UTF-8, error handling)
- Deployed to production. User approved.
```

### Decision Pattern

**Before:**
```
We discussed using PostgreSQL vs MongoDB. User asked about scaling, I explained
PostgreSQL handles vertical scaling better. User mentioned they have experience
with Postgres. We agreed to use PostgreSQL.
```

**After:**
```
## Decision: Use PostgreSQL
- Rationale: Vertical scaling, team familiarity
- Status: Agreed 2026-03-25
```

### Tool Output Pattern

**Before:**
```
Tool result: [400 lines of debug output including stack traces,
configuration dumps, and intermediate values...]
```

**After:**
```
Tool: Completed successfully
- Output: 5 files created, 3 modified
- Errors: None
- Next: Verify deployment
```

## Archive Notation

When archiving sections of context, use:

```markdown
[[archived:memory/2026-03-25-session.md#decisions]]
```

This allows recovery without keeping full context in memory.

## Density Optimization Rules

1. **One concept per line** — Don't paragraph
2. **Outcome-focused** — What happened, not how
3. **Active voice** — "Built X" not "X was built"
4. **Named references** — "The auth PR" not "the PR we discussed"

## Recovery Protocol

When you need to recover archived context:

1. Check for `[[archived:...]]` references in current context
2. Load the referenced file and line
3. Incorporate only what's relevant to current task
4. Update reference if context has evolved

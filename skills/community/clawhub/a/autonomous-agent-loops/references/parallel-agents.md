# Parallel Agents — Spec-Driven Generation

> ## ⚠️ Read Before Use
>
> This pattern launches multiple agents **simultaneously**, each writing to disk. Without worktree isolation and path validation, two agents can overwrite each other's files, leak paths into prompts, or exfiltrate spec contents. Three rules:
>
> 1. **Each agent gets its own worktree** (or at minimum, its own subdirectory under `.parallel/<run-id>/`).
> 2. **Output paths must be validated.** No `~`, no `..`, no `/tmp`, no absolute paths outside the repo. The orchestrator rejects unsafe paths.
> 3. **Spec text and directory listings are redacted** before being passed to an agent. API keys, tokens, customer IDs, internal URLs, and `.env` contents are stripped.

Deploy N agents in parallel, each generating unique output from a shared spec. Prevents duplicate concepts and enables high-throughput generation.

## Architecture

```text
Spec File (validated + redacted)
    │
    ▼
Orchestrator Agent
  ├─ Read spec
  ├─ Scan existing outputs
  ├─ Plan creative directions
  └─ Deploy N agents in parallel (each in isolated worktree)
         │
    ┌────┼────┐
    ▼    ▼    ▼
 Agent1 Agent2 Agent3  (each in .parallel/<run-id>/agent-N/)
  │      │      │
  ├─ Each receives:
  ├─  - Redacted spec text
  ├─  - Iteration number (prevents conflicts)
  ├─  - Unique creative direction
  └─  - Snapshot of existing work
         │
    ┌────┼────┐
    ▼    ▼    ▼
 Output1 Output2 Output3  (validated paths, no escapes)
```

## The Pattern

### Phase 1: Spec Analysis + Redaction

```bash
claude -p "Read /specs/component.md. Understand what component to generate."
```

Before passing the spec to agents in Phase 4, the orchestrator runs a redaction pass:

```bash
# Strip known secret patterns
sed -E 's/(api[_-]?key|token|secret|password)[=:]["a-zA-Z0-9]+/\1=REDACTED/g' spec.md > spec.redacted.md
# Remove absolute paths outside the repo
sed -E 's|/Users/[^[:space:]]+|~/REDACTED|g; s|/home/[^[:space:]]+|~/REDACTED|g' spec.redacted.md > spec.redacted.md
```

### Phase 2: Directory Scan

```bash
ls .parallel/<run-id>/ 2>/dev/null | sort -V | tail -1
# Find highest iteration number → start at N+1
```

### Phase 3: Plan Creative Directions

```bash
claude -p "
The spec: {REDACTED spec text}
Existing iterations: {list of directories}
Plan 5 UNIQUE creative directions for implementing this, each different theme.
Output: numbered list with each direction described in 1-2 sentences.
"
```

### Phase 4: Deploy Agents (Isolated)

```bash
RUN_ID=$(uuidgen)
mkdir -p ".parallel/${RUN_ID}"

for i in {1..5}; do
  direction=$(echo "$directions" | sed -n "${i}p")
  
  # Per-agent worktree (REQUIRED)
  git worktree add ".parallel/${RUN_ID}/agent-${i}" -b "parallel/${RUN_ID}/agent-${i}"
  
  (
    cd ".parallel/${RUN_ID}/agent-${i}"
    claude -p "
    Redacted spec: $(cat ../spec.redacted.md)
    Creative direction: $direction
    Iteration number: $((N+i))
    Other iterations: $(ls ../ 2>/dev/null)
    
    Generate output unique to this direction.
    Save ONLY to this directory: .parallel/${RUN_ID}/agent-${i}/
    Do NOT write to any path outside this directory.
    " &
  )
done

wait
echo "Generated iterations $N to $((N+4)) in .parallel/${RUN_ID}/"
```

## Preventing Duplicates

**Don't rely on agents to self-differentiate.** Explicitly assign each agent:

- A numbered iteration slot (no conflicts)
- A unique creative direction (no concept overlap)
- A snapshot of existing work (for uniqueness awareness)
- An isolated worktree (no file-system conflicts)

## Path Validation (REQUIRED)

The orchestrator MUST validate every path an agent writes to. Reject:

- Absolute paths (`/foo`, `~/foo`)
- Paths containing `..`
- Paths outside `.parallel/<run-id>/agent-N/`
- Symlinks pointing outside the worktree

If validation fails, the agent is killed and the error is logged. Do not let agents write wherever they want.

## Batching Strategy

| Count | Strategy |
|-------|----------|
| 1-5 | All simultaneously (one worktree each) |
| 6-20 | Batches of 5, sequential |
| infinite | Waves of 3-5, progressive depth |

## Example: Component Generation

```bash
#!/bin/bash

SPEC="specs/card-component.md"
RUN_ID=$(uuidgen)
WORKDIR=".parallel/${RUN_ID}"

# Phase 1: Redact spec
mkdir -p "$WORKDIR"
sed -E 's/(api[_-]?key|token|secret|password)[=:]["a-zA-Z0-9]+/\1=REDACTED/g' "$SPEC" > "$WORKDIR/spec.redacted.md"

# Phase 2: Find iteration number
iteration=$(ls ".parallel/" 2>/dev/null | sort -V | tail -1 | sed "s/${RUN_ID}//")
iteration=$((${iteration:-0} + 1))

# Phase 3: Plan directions
directions=$(claude -p "From spec, plan 3 unique design directions:
$(cat "$WORKDIR/spec.redacted.md")

Output: numbered list only.")

# Phase 4: Deploy agents (each in own worktree)
for i in {1..3}; do
  direction=$(echo "$directions" | sed -n "${i}p")
  
  git worktree add "${WORKDIR}/agent-${i}" -b "parallel/${RUN_ID}/agent-${i}"
  
  (
    cd "${WORKDIR}/agent-${i}"
    claude -p "
    Redacted spec: $(cat "../spec.redacted.md")
    Creative direction: $direction
    Iteration: $(($iteration + $i - 1))
    
    Generate a React component unique to this direction.
    Save ONLY inside this directory.
    " &
  )
done

wait
echo "Generated in $WORKDIR"
```

## Key Insight: Assignment Over Emergence

Don't expect agents to naturally diversify. You must:

1. Assign iteration numbers (prevents overwrite conflicts)
2. Assign creative directions (prevents concept duplication)
3. Share existing work snapshot (enables uniqueness awareness)
4. Assign isolated worktrees (prevents file-system conflicts)
5. Validate all output paths (prevents escape from sandbox)

With explicit assignment, parallel agents produce truly diverse outputs.

## When to Use Parallel Agents

✅ High-throughput content generation
✅ Need many variations of same concept
✅ Exploring design space
✅ Spec is complete and stable

❌ Interdependent work (use Sequential)
❌ Merge coordination needed (use DAG)
❌ Code changes affecting same files (use DAG)
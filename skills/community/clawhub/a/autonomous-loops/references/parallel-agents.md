# Parallel Agents — Spec-Driven Generation

Deploy N agents in parallel, each generating unique output from a shared spec. Prevents duplicate concepts and enables high-throughput generation.

## Architecture

```text
Spec File
    │
    ▼
Orchestrator Agent
  ├─ Read spec
  ├─ Scan existing outputs
  ├─ Plan creative directions
  └─ Deploy N agents in parallel
         │
    ┌────┼────┐
    ▼    ▼    ▼
 Agent1 Agent2 Agent3
  │      │      │
  ├─ Each receives:
  ├─  - Full spec text
  ├─  - Iteration number (prevents conflicts)
  ├─  - Unique creative direction
  └─  - Snapshot of existing work
         │
    ┌────┼────┐
    ▼    ▼    ▼
 Output1 Output2 Output3
```

## The Pattern

### Phase 1: Spec Analysis

```bash
claude -p "Read /specs/component.md. Understand what component to generate."
```

### Phase 2: Directory Scan

```bash
ls output_dir | sort -V | tail -1
# Find highest iteration number → start at N+1
```

### Phase 3: Plan Creative Directions

```bash
claude -p "
The spec: {full spec text}
Existing iterations: {list of directories}
Plan 5 UNIQUE creative directions for implementing this, each different theme.
Output: numbered list with each direction described in 1-2 sentences.
"
```

### Phase 4: Deploy Agents

```bash
for i in {1..5}; do
  direction=$(echo "$directions" | sed -n "${i}p")
  
  claude -p "
  Spec: {full spec text}
  Creative direction: $direction
  Iteration number: N+$i
  Existing iterations: {snapshot}
  
  Generate output unique to this direction.
  Save to: output_dir/iteration-$(($N+$i))
  " &
done

wait
```

## Preventing Duplicates

**Don't rely on agents to self-differentiate.** Explicitly assign each agent:

- A numbered iteration slot (no conflicts)
- A unique creative direction (no concept overlap)
- A snapshot of existing work (for uniqueness awareness)

## Batching Strategy

| Count | Strategy |
|-------|----------|
| 1-5 | All simultaneously |
| 6-20 | Batches of 5, sequential |
| infinite | Waves of 3-5, progressive depth |

## Example: Component Generation

```bash
#!/bin/bash

SPEC="specs/card-component.md"
OUTPUT="src/components/generated"

# Phase 1: Read spec
spec_text=$(cat "$SPEC")

# Phase 2: Find iteration number
iteration=$(ls "$OUTPUT" 2>/dev/null | sort -V | tail -1 | sed 's/iteration-//')
iteration=$((${iteration:-0} + 1))

# Phase 3: Plan directions
directions=$(claude -p "From spec, plan 3 unique design directions:
$spec_text

Output: numbered list only.")

# Phase 4: Deploy agents
for i in {1..3}; do
  direction=$(echo "$directions" | sed -n "${i}p")
  
  claude -p "
  Component spec: $spec_text
  
  Creative direction: $direction
  
  Iteration: $(($iteration + $i - 1))
  
  Other iterations: $(ls $OUTPUT 2>/dev/null)
  
  Generate a React component unique to this direction.
  Save to: $OUTPUT/iteration-$(($iteration + $i - 1))/Component.tsx
  " &
done

wait
echo "Generated iterations $iteration to $(($iteration + 2))"
```

## Key Insight: Assignment Over Emergence

Don't expect agents to naturally diversify. You must:

1. Assign iteration numbers (prevents overwrite conflicts)
2. Assign creative directions (prevents concept duplication)
3. Share existing work snapshot (enables uniqueness awareness)

With explicit assignment, parallel agents produce truly diverse outputs.

## When to Use Parallel Agents

✅ High-throughput content generation
✅ Need many variations of same concept
✅ Exploring design space
✅ Spec is complete and stable

❌ Interdependent work (use Sequential)
❌ Merge coordination needed (use DAG)
❌ Code changes affecting same files (use DAG)

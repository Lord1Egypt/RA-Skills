# Signal Memory ⚡

**Status:** 📋 Agent Guideline | **Module:** signal | **Part of:** Agent Brain

Conflict detection. The agent SHOULD call `conflicts` before storing new facts — this is a manual step, not automatic.

## When to Run Signal

Signal is NOT automatic. The agent must explicitly call it:

1. **Before storing a new fact**: Run `./scripts/memory.sh conflicts "<content>"` before `add`
2. **On-demand**: User asks "check for conflicts" or "anything inconsistent?"

```bash
# Before adding any new entry:
./scripts/memory.sh conflicts "User prefers Python for data work"

# If NO_CONFLICTS → proceed with add
# If POTENTIAL_CONFLICTS → ask user or supersede
```

## How Conflict Detection Works

The engine filters out common stopwords (I, the, is, etc.) and compares meaningful words between the new content and existing entries. A potential conflict requires:

- At least 2 meaningful words overlapping
- The overlap covering at least 30% of the shorter text's meaningful words

This prevents false positives like "I like Python" vs "Python is a snake" (different context, only 1 meaningful word overlap after filtering "I", "is", "a").

## Conflict Types

### Direct Contradiction
```
Existing: "User prefers TypeScript"
New:      "User prefers Python"
→ Ask: "Previously you said you prefer TypeScript. Has that changed?"
```

### Temporal Update
```
Existing: "Alex works at CompanyA"
New:      "Alex works at CompanyB"
→ Not a conflict — supersede the old entry
→ Run: ./scripts/memory.sh supersede <old_id> <new_id>
```

### Context-Dependent
```
Existing: "Use short responses"
New:      "Give me detailed analysis"
→ Not a conflict — different contexts
→ Store both with context:
  ./scripts/memory.sh add preference "Short responses" user "style" "" "casual chat"
  ./scripts/memory.sh add preference "Detailed analysis" user "style" "" "research tasks"
```

## Detection Flow

```
New content arrives
       │
       ▼
  conflicts <content>
       │
       ├── NO_CONFLICTS → proceed with store
       │
       └── POTENTIAL_CONFLICTS (with overlap %)
              │
              ├── Same topic, different claim? → Ask user
              ├── Same topic, newer info? → Supersede
              └── Different context? → Store both with context field
```

## Response Templates

### Contradiction Found
```
"I have something that might conflict with this:
 - Previously: [old claim]
 - Now: [new claim]
 Should I update, or are both true in different contexts?"
```

### User Corrects You
```
"Got it, tracking that correction."
→ ./scripts/memory.sh correct <old_id> "<new_content>" "<reason>"
```

## What Signal Does NOT Do

- Run automatically before stores (agent must call it manually)
- Monitor "tone shifts" (that's Vibe guidelines)
- Track confidence (that's Gauge guidelines)
- Run continuously in the background
- Detect "implicit" conflicts from silence or repeated questions

## Integration

- **Archive**: Agent should call `conflicts` before `add` (not automatic)
- **Gauge**: Conflicts may warrant downgrading confidence to UNCERTAIN

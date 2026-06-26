# Dream Consolidation Prompts

This file contains prompt templates used during the consolidation process.

## Core Consolidation Prompt

```
You are performing memory consolidation for an AI assistant. Your task is to analyze 
recent interaction fragments and distill them into refined, non-redundant memories.

## Input
Recent interactions from the past period:
{PERTINENT_INTERACTIONS}

Current long-term memories (MEMORY.md):
{LONG_TERM_MEMORIES}

Current index (memory/index.json):
{INDEX_JSON}

## Task
1. Identify FACTS, PREFERENCES, DECISIONS from interactions
2. Compare with existing memories — skip duplicates (semantic dedup)
3. Update existing entries if new information is more relevant
4. Add truly new entries to the correct MEMORY.md section
5. Update memory/index.json with new/updated entry metadata
6. Mark processed daily logs with <!-- consolidated --> at end

## Output Format
Provide your analysis:

### New Memories to Create
- [section] [one-line summary]

### Memories to Update
- [existing summary] → [updated summary]

### Memories to Archive (low importance, stale)
- [entry] — reason

### Index Updates
```json
[
  {"id": "mem_NNN", "action": "create/update/archive", "summary": "..."}
]
```

## Safety Rules
- Never delete original daily logs
- Never remove ⚠️ PERMANENT entries
- If MEMORY.md changes >30%, save .bak first
```

## Stage-Specific Prompts

### Orient Stage
```
Survey the memory system:
1. Count files in memory/ directory
2. Count entries in MEMORY.md by section
3. Read index.json for health stats
4. Identify: duplicates, stale entries, gaps

Output as structured markdown.
```

### Gather Stage
```
Review recent daily logs (last 7 days, memory/YYYY-MM-DD.md):
Extract and categorize:
1. Decisions made (choices, direction changes)
2. Key facts (metrics, data, technical details)
3. Progress (milestones, blockers, completions)
4. Lessons (failures, wins, insights)
5. Todos (unfinished, pending)

Skip: casual conversation, obvious things, things already in MEMORY.md
```

### Consolidate Stage
```
Compare extracted items with MEMORY.md:
- New → append to correct section
- Updated → modify existing entry (newer data wins)
- Duplicate → skip (check meaning, not just text)
- Procedures → append to memory/procedures.md

Update index.json with entry metadata.
```

### Prune Stage
```
Find entries eligible for archival:
- 90+ days since last referenced
- Importance < 0.3
- Not marked 📌 PIN or ⚠️ PERMANENT
- Not in episodes/

For each eligible entry:
1. Compress to one-line summary
2. Move to memory/archive.md
3. Set archived=true in index.json
```

## Health Score Prompt

```
Compute 5-metric health score:

1. Freshness: grep lastReferened in last 30 days / total entries
2. Coverage: sections updated in last 14 days / 10 sections
3. Coherence: entries with related links / total
4. Efficiency: max(0, 1 - MEMORY.md_lines/500)
5. Reachability: compute connected components in relation graph

health = (freshness×0.25 + coverage×0.25 + coherence×0.2 + efficiency×0.15 + reachability×0.15) × 100
```

## Quality Checklist

A good memory entry:
- [ ] Has clear section (Core Identity, User, Projects, etc.)
- [ ] Is specific rather than generic
- [ ] Includes the "why" behind rules
- [ ] Is not derivable from reading code/files
- [ ] Will be relevant for future sessions
- [ ] Is concise (under 500 words)
- [ ] Has importance marker if needed (🔥 HIGH, 📌 PIN, ⚠️ PERMANENT)

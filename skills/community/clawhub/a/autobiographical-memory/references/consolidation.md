# Consolidation Reference

This file provides detailed guidance for the consolidation workflow.

## Full Consolidation Run

A thorough consolidation, recommended every 7 days:

```python
# Pseudocode for the consolidation process
1. Collect all memory/*.md files
2. Sort by modification time (newest first)
3. Read the N most recent files (N = days since last consolidation + 2)
4. For each file:
   a. Extract sections: Events, Decisions, Observations, Notes
   b. Classify each item:
      - PERSISTENT: user preferences, decisions with long-term impact, lessons
      - PROJECT: ties to an active project
      - SOCIAL: relationship details, important interactions
      - TRANSIENT: one-off status updates, routine mentions
   c. For PERSISTENT items → propose addition to MEMORY.md
   d. For PROJECT items → update relevant project context
   e. For TRANSIENT items → leave in daily note, don't promote
5. Check MEMORY.md for:
   - Duplicates (same info already there)
   - Stale entries (old projects, reversed preferences)
   - Outdated information
6. Write updated MEMORY.md with consolidated content
```

## Lightweight Consolidation (Heartbeat)

A quick check, suitable for every heartbeat cycle:

```
1. Read today's daily note if it exists
2. Scan for any MUST-REMEMBER items
3. If found, update MEMORY.md immediately
4. Otherwise, skip
```

## Categorization Heuristics

| Cue | Likely Category | Action |
|-----|----------------|--------|
| "I prefer/like/don't like..." | PERSISTENT | Add to MEMORY.md |
| "We decided to..." | PERSISTENT | Add to MEMORY.md |
| "The project X is..." | PROJECT | Update project context |
| "[X person] said..." | SOCIAL | Add if significant relationship |
| "Today I checked..." | TRANSIENT | Leave in daily note |
| "I learned that..." | PERSISTENT | Add to MEMORY.md if broadly useful |

# Recall Patterns Reference

## Search Query Strategies

### Single Domain Search
When you know the domain but not the exact terms:
```
memory_search(query="task name status")     # Too specific
memory_search(query="task project alpha")   # Better — broader terms
memory_search(query="project status")       # Also try
```

### Temporal Search
When you know roughly when something happened:
```
# If today is April 2026, try:
memory_get(path="memory/2026-04-*.md")  # Globbing not supported, use specific dates
memory_get(path="memory/2026-04-15.md")
memory_get(path="memory/2026-04-14.md")
```

### Multi-angle Search
If the first search is weak, try different phrasing:
```
memory_search(query="user name preference")  → weak
memory_search(query="preferred tool")        → try
memory_search(query="what they like")        → try
```

## Priority-Sensitive Recall

**High priority** — always check MEMORY.md + recent daily notes:
- User preferences and stated dislikes
- Active project context
- Recent decisions (<7 days)

**Medium priority** — check MEMORY.md + search daily notes:
- Technical environment quirks
- Social relationships
- Lessons learned

**Low priority** — search only, don't proactively read:
- Obsolete project details
- Routine logs

## Cross-File Memory

Some information lives outside `memory/`:

| File | Stores | When to Check |
|------|--------|--------------|
| MEMORY.md | Long-term curated | Always, before every task |
| USER.md | User identity | When understanding context |
| SOUL.md | Agent identity | When deciding tone/manner |
| TOOLS.md | Environment specifics | When referencing tools |
| IDENTITY.md | Agent persona | When communicating style matters |
| AGENTS.md | Core rules | When uncertain about protocols |
| memory/*.md | Raw logs | When MEMORY.md lacks detail |

## Recovery from Weak Recall

If memory_search returns nothing useful:

1. **Ask specifically**: "I checked my records — do you remember when we discussed this? A rough date would help me find it."
2. **Accept the gap**: Sometimes you just don't have it. Say so.
3. **Start fresh**: Record the new information properly so future-you has it.

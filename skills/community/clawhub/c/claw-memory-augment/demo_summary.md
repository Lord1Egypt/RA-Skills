# Memory Augment Demo Summary

This file demonstrates what memories look like after running the memory-augment skill.

## Sample Memories

```yaml
memories:
  - id: test-001
    type: preference
    content: "User prefers Python for automation scripts"
    tags: ["coding", "python", "automation"]
    score: 0.95
    
  - id: test-002
    type: decision
    content: "Approved inbox-triage skill for publishing"
    tags: ["income", "skills", "approval"]
    score: 0.98
    
  - id: test-003
    type: context
    content: "Building memory-augment skill, 60% complete"
    tags: ["project", "development"]
    score: 0.85
    
  - id: test-004
    type: learning
    content: "Sub-agent spawning reduces context by ~30%"
    tags: ["pattern", "optimization"]
    score: 0.88
    
  - id: test-005
    type: preference
    content: "User is in UTC timezone"
    tags: ["timezone", "config"]
    score: 0.92
```

## Sample Search Query

Query: `"what did I decide about income"`

Results:
```
### decision (score: 0.98)
**Content:** Approved inbox-triage skill for publishing
**Tags:** income, skills, approval
**Created:** 2026-04-15
```

## Auto-Inject Context Example

When discussing "skills" or "income", the agent would automatically inject:

```json
{
  "context": {
    "memories": [
      {
        "topic": "income-decision",
        "content": "User approved inbox-triage for publishing to clawhub"
      },
      {
        "topic": "preferences", 
        "content": "User prefers Python for automation scripts"
      }
    ]
  }
}
```

## Usage Example

```bash
# Store a memory
clawhub memory store "User prefers minimal markdown formatting" \
  --type preference --tag preferences

# Search for it
clawhub memory search "markdown preferences"

# List all preferences
clawhub memory list --type preference

# Summarize last 7 days
clawhub memory summarize --since "7 days ago"
```

---

**Status:** Skill in development (~60% complete)
**Next:** Complete packaging and test suite

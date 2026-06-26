# auto-skill-extractor

Automatically learn from your AI's work and turn repeated subagent tasks into reusable skills.

## Description

Watches subagent completions, detects patterns worth reusing, and creates draft skills automatically. After 3 successful re-invocations, drafts are promoted to active skills.

## How It Works

1. **Trigger**: After every subagent completion, the main agent calls `scripts/auto-skill-trigger.py`
2. **Score**: Complexity is calculated (tool calls × 0.7, +2 for multi-domain, +2 for error recovery)
3. **Extract**: If score ≥ 4 and ≥ 3 tool calls → create DRAFT skill in `skills/auto-draft/`
4. **Evaluate**: After 3 successful re-invocations → promote to `skills/auto/`
5. **Archive**: Drafts unused for 7+ days → archived

## Integration

Add to AGENTS.md or your agent's completion handler:

```python
# After subagent completion
import subprocess, json

trigger_input = {
    "completion_status": "success",  # or "failed", "timeout"
    "tool_calls": tool_call_count,
    "session_id": session_key,
    "multi_domain": True,  # if task crossed domains (files + web + system)
    "transcript_summary": brief_summary  # keep brief, no secrets
}

# Method 1: Stdin (recommended, no file on disk)
result = subprocess.run(
    ["python3", "scripts/auto-skill-trigger.py"],
    input=json.dumps(trigger_input),
    capture_output=True, text=True
)

# Method 2: File (delete immediately after)
with open("/tmp/trigger.json", "w") as f:
    json.dump(trigger_input, f)
result = subprocess.run(["python3", "scripts/auto-skill-trigger.py", "/tmp/trigger.json"], capture_output=True)
os.remove("/tmp/trigger.json")
```

## Directives

- `#skill: <name>` — Manually trigger extraction from last subagent
- `#skill: force` — Force extraction (ignore thresholds)

## Commands

```bash
# List active auto-skills
python3 scripts/skill-lifecycle.py list

# List drafts under evaluation
python3 scripts/skill-lifecycle.py drafts

# Process promotions and archives
python3 scripts/skill-lifecycle.py process

# Manually promote a draft
python3 scripts/skill-lifecycle.py promote my-skill-name
```

## Complexity Scoring

| Factor | Points | Example |
|--------|--------|---------|
| Tool calls × 0.7 | 2-5 pts | 3 tools = 2, 5 tools = 4 |
| Multi-domain | +2 pts | Files + web + system |
| Error recovery | +2 pts | Retry on failure |

**Threshold:** 4 points = creates DRAFT

## Directory Structure

```
skills/
├── auto-draft/          # Draft skills (under evaluation)
│   └── {name}-{hash}/
│       ├── SKILL.md
│       └── meta.json
├── auto/                # Promoted skills (ready to use)
│   └── {skill-name}/
│       ├── SKILL.md
│       └── promotion.json
└── manual/              # Hand-crafted skills
```

## Configuration

- `COMPLEXITY_THRESHOLD = 4` — Lower = more drafts, more curation needed
- `PROMOTE_THRESHOLD = 3` — Re-invocations before promotion
- `ARCHIVE_AGE_DAYS = 7` — Days before unused drafts archived
- `MAX_QUEUE_SIZE = 50` — Pending extraction limit

## Safety

- ✅ No sensitive data persisted (only tool counts, scores, timestamps)
- ✅ Session IDs are hashed, not stored raw
- ✅ Path traversal prevention on skill names
- ✅ Atomic promotions (copy → verify → move)
- ✅ Queue limits (max 50 pending)
- ✅ No transcript content written to disk

## Companion Skills

- **subagent-orchestration** — The subagent pattern that generates the work this skill extracts from
- **skill-creator** — For manually creating or improving skills
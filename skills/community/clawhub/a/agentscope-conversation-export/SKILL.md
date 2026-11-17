---
name: agentscope-conversation-export
description: Export AgentScope conversation histories to JSON, Markdown, CSV, or HTML. Use this when the user wants to share, review, archive, or analyze multi-turn agent dialogues outside the runtime.
version: 0.1.0
metadata:
  openclaw:
    requires:
      env: []
      bins:
        - python3
    primaryEnv: ""
    envVars: []
    emoji: "📤"
    homepage: https://github.com/agentscope-ai/agentscope
---

# AgentScope Conversation Export

This skill converts AgentScope conversation logs into shareable formats. It supports:

- JSON export for programmatic reuse
- Markdown export for human review
- CSV export for analysis
- HTML export for browser review

## What this skill does

- Reads AgentScope dialog/session logs
- Normalizes turns and metadata
- Exports to multiple formats
- Preserves timestamps, roles, and tool calls

## How to use

Run the exporter script from this skill folder:

```bash
python3 scripts/export_conversation.py --input /path/to/dialog.json --format markdown --output /tmp/conversation.md
```

Supported formats:

- `json`
- `markdown`
- `csv`
- `html`

## Security notes

- Exported files may contain conversation content; review before sharing
- No external network calls are made
- Input paths are resolved locally

## Troubleshooting

- If the input file is missing, verify the AgentScope dialog path
- For large histories, export to JSON first, then convert

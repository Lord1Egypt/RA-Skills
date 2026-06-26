# OpenClaw Integration

## Platform-Specific Notes

### Installation

OpenClaw can use llm-wiki in two modes:

1. **Protocol Mode** (Recommended)
   - No installation required
   - Agent reads `CLAUDE.md` and operates on files directly
   - Use natural language: "请摄入资料"

2. **CLI Mode** (Optional)
   - Install Python dependencies: `pip install -r src/requirements.txt`
   - Use for scripting: `./scripts/wiki-status.sh`

### Skill Registration

To register llm-wiki as an OpenClaw skill:

1. Upload `SKILL.md` to OpenClaw skill registry
2. Reference `CLAUDE.md` as the primary protocol
3. Optional: Configure hooks in `HOOKS.md`

### Natural Language Triggers

| Intent | Example Trigger |
|--------|-----------------|
| Ingest | "请摄入 sources/paper.pdf" |
| Query | "查询 wiki 关于 Transformer 的内容" |
| Lint | "检查 wiki 健康状况" |
| Status | "wiki 状态怎么样" |

### Differences from Claude Code

- OpenClaw may have different file system permissions
- Check `AGENTS.md` for environment detection logic
- Both platforms use the same `CLAUDE.md` protocol

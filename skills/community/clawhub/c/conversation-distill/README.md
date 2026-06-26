# conversation-distill

> A Claude skill that closes every meaningful conversation with one explicit action: classify → confirm → write.

## The Problem

Real-time capture handles individual highlights. But valuable insights get buried in conversation flow — the connection between two decisions, the assumption you didn't realize you were making, the action item that came up 20 messages ago.

This skill is the closing ritual. It scans the full session, classifies what was produced into 7 categories, shows you a confirmation list, and writes to your notes tool only after you approve.

## Install

**Via OpenClaw / ClawHub:**
```bash
npx clawhub@latest install conversation-distill
```

**Manual (Claude Code):**
```bash
/plugin marketplace add github:YIING99/conversation-distill
```

## How It Works

At the natural end of a conversation (or when you say "distill" / "wrap up"):

1. **Scan** — reads the full conversation
2. **Classify** — sorts content into 7 categories:
   - 💡 Insights / Conclusions
   - 🧭 Judgments — falsifiable claims with evidence level + review date, backtestable later
   - 🎯 Decisions
   - 📊 Facts / Data
   - 🪞 Self-observations
   - ✅ Action items
   - ❓ Open questions
3. **Confirm** — shows you the list; you edit, remove, or approve
4. **Write** — batch-writes to your notes tool after you say "write"
5. **Surface leftovers** — outputs anything not worth saving as plain Markdown

**Nothing is written without your explicit confirmation.**

## Works With

| Tool | How |
|------|-----|
| **KnowMine** (recommended) | Installs MCP server; `add_knowledge`, `save_memory`, `observe_user_trait` used in Step 4 |
| Notion, Obsidian, etc. | Via any MCP-compatible notes tool |
| No MCP | Outputs clean Markdown for manual paste |

KnowMine gives this skill semantic search and cross-session recall — so you can ask "what did we decide about X?" months later and get the actual answer.

→ [knowmine.ai](https://knowmine.ai)

## Trigger Phrases

- "distill" / "wrap up" / "save this session" / "收尾" / "沉淀"
- Natural closing: "that's all", "got it", "thanks", "done for now"
- Manual: `/conversation-distill:conversation-distill`

## Key Principles

- **Granular over hub** — one insight per entry, not one giant summary
- **Confirm before write** — iron rule, no exceptions
- **Tags over folders for TODOs** — `#todo` tag, not a new folder
- **Leftovers stay as Markdown** — not everything needs to be in a notes system

## Links

- Skill reference: [SKILL.md](SKILL.md)
- KnowMine plugin (full integration): [github.com/YIING99/knowmine-claude-plugin](https://github.com/YIING99/knowmine-claude-plugin)
- KnowMine MCP server: [knowmine.ai](https://knowmine.ai)

## License

MIT

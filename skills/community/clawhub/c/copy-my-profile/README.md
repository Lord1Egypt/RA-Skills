# copy-my-profile

> Portable Markdown profile for AI tools. Like vCard for contacts — but for
> your AI assistant's understanding of you.

## What it does

Extract a standardized profile from any AI tool's long-term memory, then
re-use it in another tool without retraining.

**The problem**: You spent weeks teaching Claude Code your preferences. Now
you want to use Cursor at work. Cursor knows nothing about you. Tomorrow you
try Codex CLI on your home server — same blank slate.

**The fix**: Run this skill in Tool A → get a portable `my-profile.md` →
paste into Tool B. Done.

## Five categories

| Category | What goes in |
|----------|--------------|
| **Instructions** | Explicit rules ("always do X", "never do Y", ⚠️ rules) |
| **Identity** | Name, education, interests (non-sensitive only) |
| **Profession** | Role, company, skill domains |
| **Projects** | Projects you're actually building |
| **Preferences** | Work style and taste preferences |

## Supported tools (read FROM)

Claude Code · OpenClaw · Codex CLI · Cursor · Cline · Continue · Aider · any
LLM agent with file access

## Supported tools (write TO)

All of the above + ChatGPT web + Claude.ai web (see
`references/import-prompts.md` for tool-specific import prompts)

## Usage

In any supported AI tool, say:

> Generate my profile.

The skill will:

1. Auto-detect the host tool's memory files (or ask you to paste them)
2. Extract entries into 5 categories with `[YYYY-MM-DD] - entry` format
3. Write the output to `./my-profile.md` AND show it inline
4. Tell you which file to paste it into for your target tool

## Privacy

- All processing is local — nothing leaves your machine
- The skill filters out IDs, passwords, tokens, financial details, and family
  info automatically (see `references/profile-template.md`)
- You see the full output before copying anywhere

## Cross-tool transfer

| Direction | How |
|-----------|-----|
| **Pull** (export) | Run this skill, copy `my-profile.md` |
| **Push** (import) | Use the prompts in `references/import-prompts.md` |
| **Mirror** (multi-device) | Stash `my-profile.md` in Notion / iCloud Drive / GitHub gist |

## Files

```
copy-my-profile/
├── SKILL.md                              ← agent entry point
├── README.md                             ← this file
├── LICENSE                               ← MIT
└── references/
    ├── profile-template.md               ← output format + privacy rules
    ├── tools-memory-map.md               ← where each tool stores memory
    └── import-prompts.md                 ← copy-paste prompts per target tool
```

## License

MIT — see [LICENSE](./LICENSE).

## Author

Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)

---
name: chat-memory-archiver
description: "Extract decisions, todos, knowledge, preferences, and risks from AI chat sessions into structured memory"
---

# Session Archiver

Parse AI chat session logs and extract structured knowledge: decisions made, pending todos, learned facts, user preferences, and flagged risks. Merge across sessions and export to Markdown, JSON, Obsidian, or Notion.

## Workflow

1. **Parse conversation** — Read session log, extract question-answer pairs, tool calls, and decision points.
2. **Segment by phase** — Label each segment as problem / exploration / decision / action.
3. **Extract 5 categories**:
   - 📌 **Decisions** — Choices made, with rationale and alternatives considered.
   - ✅ **Todos** — Action items, owners, and deadlines.
   - 📚 **Knowledge** — Facts, code snippets, links, and explanations.
   - ⭐ **Preferences** — User style, terminology, tools, conventions.
   - ⚠️ **Risks** — Security concerns, known issues, caveats.
4. **De-duplicate & merge** — Fuse repeated information across multiple sessions, keep latest version.
5. **Topic tagging** — Auto-tag each session with relevant domain labels (e.g. `#python`, `#api-design`, `#deployment`).
6. **Cross-session graph** — Build lightweight association graph showing which sessions share topics or reference each other.
7. **Format export** — Generate output in Markdown, JSON, Obsidian-flavored wiki links, or Notion JSON.
8. **Summary** — Produce a concise 5-sentence summary of each session for quick scanning.

## Sample Prompts

- `session-archiver extract --sessions session-2026-06-01.log session-2026-06-02.log`
- `session-archiver extract --sessions . --format obsidian --outdir ./vault`
- `session-archiver merge --sessions . --dedup --out summary.json`
- `session-archiver report --sessions . --graph > session-graph.dot`

## Safety

- Session logs are parsed locally; never sent to external services.
- Sensitive content (passwords, keys) in logs is flagged during extraction; user must explicitly confirm before inclusion in output.

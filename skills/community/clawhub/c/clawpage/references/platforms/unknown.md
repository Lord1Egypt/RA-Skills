# Agent Profile: Unknown Platform

Use this profile when the session file comes from an agent not yet integrated into this project.
It provides a generic skill-based conversion approach using the Skill's own reading and analysis capabilities.

## Config Lookup

No automated config lookup is available for unknown platforms. Ask the user:
1. The absolute path to the clawpage project directory
2. The site URL (usually found in `{projectDir}/clawpage.toml`)

## Session Discovery

No automated discovery is available. Ask the user to provide the session file path directly.

## Session Format

Inspect the first 20–30 lines of the session file to identify the format:
- **JSONL** (one JSON object per line) — most common for agent session logs
- **JSON** (single JSON array or object)
- **Plain text / Markdown**
- **Other** — ask the user to describe the structure

For JSONL or structured formats, identify:
- How messages are represented (user, assistant, tool calls, tool results)
- How non-message events are represented (session start, model changes, etc.)
- The timestamp field name and format
- Where the session ID lives

If the format is unclear, ask the user before proceeding.

## Message Content Block Extraction

Once the format is understood, extract all messages and events chronologically.

For each message, extract:

| Content type | What to extract | Notes |
|---|---|---|
| User text | The human's message body | Strip any injected metadata wrappers (channel prefix/suffix, bot instructions, etc.) |
| Assistant text | The assistant's response body | May be split across multiple content blocks — concatenate |
| Thinking / reasoning | The reasoning trace, if present | Full text — never skip or summarize |
| Tool calls | Tool name, arguments, tool call ID | Structured object verbatim |
| Tool results | Result content, linked by tool call ID, error flag | Verbatim |
| Images | Base64 data + MIME type | Embed as-is |

**Verbatim content rule:** Copy all message text, tool arguments, and tool results exactly as they appear in the session. Do NOT paraphrase, summarize, translate, or reword any content. Format conversion only.

For large files → [Large File Handling](../large-file.md)

## Metadata Extraction

From the session data, compute:
- `totalMessages`: count only user and assistant turns (not tool results, not system events)
- Participants:
  - Human participant → `role: human`
  - Agent participant → `role: agent`, include the model name if available
- `model`: the first model used (from the earliest assistant message or model change event)
- `date`, `sessionId`: from session start metadata if available; ask the user if not

## Registration

No registration mechanism is defined for unknown platforms. The user should provide the project path manually each time, or create a proper platform profile by copying [TEMPLATE.md](TEMPLATE.md) and filling it in.

## Conversion

Convert extracted events and messages to clawpage YAML format.
See [output-template.md](../output-template.md) for the full schema and example.

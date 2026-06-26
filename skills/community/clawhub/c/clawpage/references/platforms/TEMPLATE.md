# Agent Profile Template

Use this template when adding support for a new agent/platform.
Copy this file to `references/platforms/{agent-name}.md` and fill in each section.

---

## Config Lookup

Describe how to find the registered clawpage project directory for this agent.

- Where does this agent store tool/project registrations? (e.g., a config file, workspace file, env var)
- What key or section to look up?
- What to do if not found → link to [First-Time Setup](../setup.md)

Also describe where to find the `site` URL (usually `{projectDir}/clawpage.toml`).

## Session Discovery

Describe how to list and filter session files for this agent.

- Default session directory path
- File format (extension, naming convention)
- How to filter by: exact session ID, topic keyword, or "current" (most recent)
- How to present candidates for user confirmation

## Session Format

Describe the session file format (e.g., JSONL, JSON, binary).

List the event types and their key fields in a table:

| Type | Key fields |
|------|------------|
| (event type) | (field names and meaning) |

Link to any detailed schema documentation if available.

## Message Content Block Extraction

Describe the structure of a message event and how to extract each content block type.

Show the message event structure as a JSON example, then a table:

| Block `type` | Extract | Notes |
|---|---|---|
| `text` | (field) | (notes, e.g., concatenate multiple blocks) |
| `thinking` | (field) | Full reasoning text — never skip or summarize |
| `toolCall` | (fields) | (notes) |
| `image` | (fields) | (how to get base64 data and MIME type) |

If the platform injects external channel metadata into user messages, describe how to clean it here (or link to a subsection).

## Metadata Extraction

Explain how to compute:

- `totalMessages`: which event/role types count as a "message" for this field
- Participants: how roles map to human vs. agent, and where to get the model name

## External Channel Cleaning _(optional)_

If this agent injects channel-specific metadata (Discord, Telegram, etc.) into messages, document the cleaning rules here. Otherwise, omit this section.

## Registration

Describe how the user registers a clawpage project with this agent so that Config Lookup can find it.

Include the exact command or file edit needed.

## Conversion

Describe how to convert the session to clawpage YAML for this platform.

If a CLI tool handles it, show the exact command.
If the Skill does it manually, describe the extraction steps and reference [output-template.md](../output-template.md) for the output schema.

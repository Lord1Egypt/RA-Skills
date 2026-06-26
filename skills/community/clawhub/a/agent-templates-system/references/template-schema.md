# Agent Template Schema Notes

## Top-level record fields

A stored template record includes:
- `id`
- `name`
- `description`
- `category`
- `version`
- `tags`
- `definition`
- `createdAt`
- `updatedAt`

## Definition shape

```json
{
  "identity": {
    "name": "Social Media Coordinator",
    "emoji": "🧭",
    "avatar": "avatars/social-media-coordinator.png",
    "creature": "AI workflow coordinator",
    "vibe": "Organized, unflappable, deadline-aware"
  },
  "skills": [
    { "name": "copywriting" },
    { "name": "postiz", "clawhubUrl": "https://clawhub.ai/nevo-david/postiz" }
  ],
  "config": {
    "name": "Social Media Coordinator"
  },
  "workspace": {
    "files": [
      {
        "path": "SOUL.md",
        "content": "# SOUL...",
        "mode": "overwrite"
      }
    ],
    "memorySeeds": [
      {
        "path": "MEMORY.md",
        "content": "# MEMORY...",
        "mode": "overwrite"
      }
    ]
  }
}
```

## Field behavior

### `identity`
Used to populate generated identity details during agent creation.

Useful keys:
- `name`
- `emoji`
- `theme`
- `avatar`
- `creature`
- `vibe`

### `skills`
Optional list of skills to attach to the created agent.

Each item supports:
- `name`
- `clawhubUrl` optional

### `config`
Partial agent config merged into the created agent entry.

Use this for agent-level defaults. Keep it partial and focused.

### `workspace.files`
Arbitrary files to write into the created workspace.

File modes:
- `overwrite` default
- `skip-if-exists`
- `append`

Use this for:
- `SOUL.md`
- `AGENTS.md`
- checklists
- starter docs
- team instructions

### `workspace.memorySeeds`
Starter memory content to write into memory files.

Modes:
- `overwrite`
- `append`

Use this for:
- initial `MEMORY.md`
- client or role notes
- operating assumptions

## Validation / normalization notes

The implementation normalizes and trims many string fields.

Notable normalization behavior:
- tags are deduplicated case-insensitively
- blank strings are dropped
- missing file mode defaults to `overwrite`
- missing memory seed mode defaults to `append`
- invalid or empty skill names are discarded

## Safety note

Workspace file paths are checked against the target workspace root. Do not depend on path traversal or absolute writes; they will be rejected.

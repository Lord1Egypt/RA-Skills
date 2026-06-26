# Workspace Skills (Independent from Plugin)

These skills are workspace-level OpenClaw skills and are not tied to any plugin runtime.

## Included Skills

- `composition-correction` (InkCraft API-backed essay correction)

## Location

OpenClaw loads workspace skills from `./skills` with highest priority.

## Slash Command Usage

Because each skill sets `user-invocable: true`, you can call them with:

- `/composition_correction <input>`

If your channel cannot register every native skill command, fallback to:

- `/skill composition-correction <input>`

For `composition-correction`, configure API key via env in `openclaw.json`:

- `skills.entries["composition-correction"].apiKey`
- or `skills.entries["composition-correction"].env.INKCRAFT_API_KEY`
- optional `skills.entries["composition-correction"].env.INKCRAFT_BASE_URL`

## Recommended openclaw.json Snippet

```json5
{
  commands: {
    text: true,
    nativeSkills: "auto"
  },
  skills: {
    load: {
      watch: true,
      watchDebounceMs: 250
    },
    entries: {
      "composition-correction": {
        enabled: true,
        apiKey: "YOUR_INKCRAFT_API_KEY",
        env: {
          INKCRAFT_BASE_URL: "https://www.inkcraft.cn"
        }
      }
    }
  }
}
```

After adding/updating a skill, start a new session or refresh skills.

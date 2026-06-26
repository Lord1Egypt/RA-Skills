---
name: anygen-task-download
version: 1.0.0
description: "AnyGen: Download artifacts from a completed task."
metadata:
  requires:
    bins: ["anygen"]
    env: ["ANYGEN_API_KEY"]
  install:
    - id: node
      kind: node
      package: "@anygen/cli"
      bins: ["anygen"]
  cliHelp: "anygen task +download --help"
---

# task +download

> **PREREQUISITE:** Read [`../anygen-shared/SKILL.md`](../anygen-shared/SKILL.md) for auth, global flags, and security rules.

Download artifacts from a completed task.

## Usage

```bash
anygen task +download --task-id <id> --output-dir <dir>
```

## Flags

| Flag | Required | Description |
|------|----------|-------------|
| `--task-id` | ✓ | Task ID |
| `--output-dir` | — | Local directory to save files (default: current directory) |
| `--file <name...>` | — | Download specific file(s) by name (repeatable) |
| `--thumbnail` | — | Download thumbnail image instead of main files |

## Examples

```bash
# Download all output files
anygen task +download --task-id xxx

# Download specific file(s) by name
anygen task +download --task-id xxx --file report.pptx
anygen task +download --task-id xxx --file report.pptx --file data.xlsx

# Download thumbnail (for preview)
anygen task +download --task-id xxx --thumbnail

# Specify output directory
anygen task +download --task-id xxx --output-dir ./output
```

## Output

Returns JSON with downloaded file paths:

```json
{
  "status": "completed",
  "task_id": "xxx",
  "files": [
    { "file": "./report.pptx", "name": "report.pptx" },
    { "file": "./data.xlsx", "name": "data.xlsx" }
  ],
  "task_url": "https://..."
}
```

## Tips

- The task must be in `completed` state. Use `task get --wait` first if needed.
- Without `--file`, all output files are downloaded.
- Use `--thumbnail` first to show a preview, then download the main files when user requests it.
- For smart_draw tasks, diagram files are automatically rendered to PNG.
- File names for `--file` come from the `output.files[].name` field in the task get response.

> [!CAUTION]
> This is a **write** command (writes files to disk) — confirm the output directory with the user.

## See Also

- [`anygen-workflow-generate`](../anygen-workflow-generate/SKILL.md) — Full content generation workflow

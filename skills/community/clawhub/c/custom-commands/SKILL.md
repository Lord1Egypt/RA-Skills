```markdown
# custom-commands/SKILL.md

## Custom Commands

Define and manage custom commands like `backup`, `sync`, `clean`, `generate`, and `audit` for streamlined workflows.

### Commands

- `backup [path]` - Backs up files/folders to a specified location (default: cloud storage)
- `sync [source] [destination]` - Synchronizes files between locations
- `clean [pattern]` - Deletes temporary files matching a pattern
- `generate [type]` - Generate content (articles, scripts, outlines) based on prompts
- `audit [scope]` - Run security or workflow audits (e.g., "Audit content approval process")

### Integration

- Voice command support: "Hey Assistant, backup my documents" or "Write a 500-word article on AI ethics"
- Auto-suggest these commands in relevant contexts

### Memory Optimization

- **Rule 1**: Save only high-impact decisions (e.g., "Approved backup schedule: daily at 2 AM", "Adjusted content approval workflow")
- **Rule 2**: Redact IPs, credentials, or internal URLs before storing (e.g., "Client email: [REDACTED]", "Internal URL: [REDACTED]")
- **Rule 3**: Archive completed tasks to `memory/archived/` with dated filenames (e.g., `memory/archived/2026-03-18_content-review.md`)

```
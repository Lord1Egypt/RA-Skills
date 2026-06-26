# Journals

---

## Journal Module

### list

List journals in workspace.

```bash
affine-cli journal list [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --workspace | -w | No | Workspace ID |
| --count | -c | No | Number of journals to return (default: 20) |

### create

Create a new journal entry.

```bash
affine-cli journal create [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --date | -d | No | Date in YYYY-MM-DD format. Default: today |
| --content | -c | No | Journal content. Prefix `@` for file path |
| --icon | -i | No | Emoji icon (e.g., `📝`, `💭`, `🎯`) |
| --workspace | -w | No | Workspace ID |

**Examples:**
```bash
# Create today's journal
affine-cli journal create

# Create for specific date
affine-cli journal create --date 2025-04-10

# Create with content
affine-cli journal create --content "# Morning\n- Team standup\n- Code review"

# From file
affine-cli journal create --content "@journal.md"

# With icon
affine-cli journal create --icon "💭"
```

### info

Get journal details.

```bash
affine-cli journal info [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --id | -i | No* | Document ID |
| --date | -d | No* | Date in YYYY-MM-DD format |
| --workspace | -w | No | Workspace ID |

*Either `--id` or `--date` is required.

**Examples:**
```bash
# By date
affine-cli journal info --date 2025-04-10

# By ID
affine-cli journal info -i DOC_ID
```

### append

Append content to journal.

```bash
affine-cli journal append [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --id | -i | No* | Document ID |
| --date | -d | No* | Date in YYYY-MM-DD format |
| --content | -c | **Yes** | Content to append. Prefix `@` for file path |
| --workspace | -w | No | Workspace ID |

*Either `--id` or `--date` is required.

**Examples:**
```bash
# Append to today
affine-cli journal append --content "# Evening\n- Completed tasks"

# Append to specific date
affine-cli journal append --date 2025-04-10 --content "# Notes\nMeeting summary"

# Append from file
affine-cli journal append --date 2025-04-10 --content "@notes.md"
```

### update

Update journal content (replaces entire content).

```bash
affine-cli journal update [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --id | -i | No* | Document ID |
| --date | -d | No* | Date in YYYY-MM-DD format |
| --content | -c | No | New content |
| --icon | -i | No | New emoji icon |
| --workspace | -w | No | Workspace ID |

*Either `--id` or `--date` is required.

**Examples:**
```bash
# Update by date
affine-cli journal update --date 2025-04-10 --content "# Updated content"

# Update icon
affine-cli journal update --date 2025-04-10 --icon "💡"

# Update from file
affine-cli journal update --date 2025-04-10 --content "@new-content.md"
```
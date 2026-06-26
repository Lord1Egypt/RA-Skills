# Marketplace Management

Clone, list, and update plugin marketplace repositories.

## Commands

| Command | Description |
|---------|-------------|
| `clone <url>` | Clone a GitHub repo into marketplaces directory |
| `list` | List installed marketplaces with remote URLs |
| `update [name]` | Git pull one or all marketplaces |

## Paths

```
~/.claude/plugins/marketplaces/<name>/
```

## clone

```bash
git clone <url> ~/.claude/plugins/marketplaces/<repo-name>
```

- Extracts repo name from URL (last path segment, strips .git)
- If already exists → AskUserQuestion (overwrite or cancel)

## list

```bash
# For each marketplace directory
git -C <dir> remote get-url origin
```

Output format:

```
| Name | Remote URL | Last Updated |
|------|------------|--------------|
```

## update

```bash
# Single marketplace
git -C ~/.claude/plugins/marketplaces/<name> pull

# All marketplaces
for dir in ~/.claude/plugins/marketplaces/*/; do
  git -C "$dir" pull
done
```

After update: restart Claude Code to reload cached plugins.

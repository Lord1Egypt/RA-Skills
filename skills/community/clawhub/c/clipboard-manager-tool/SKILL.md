---
name: clipboard-manager
description: Clipboard history management. Use when user says "copy to clipboard", "paste from clipboard", "clipboard history", or wants to manage copied items.
---

# Clipboard Manager

Manage clipboard history with save, search, and recall capabilities.

## File Location

`clipboard-history.md` in workspace root

## Commands

### Save Current Clipboard
When user says: "save clipboard", "copy this to history"
```bash
bash skills/clipboard-manager-1.0.0/scripts/clipboard.sh save
```

### Get Current Clipboard
When user says: "what's in clipboard", "show clipboard"
```bash
bash skills/clipboard-manager-1.0.0/scripts/clipboard.sh get
```

### Set Clipboard
When user says: "copy this to clipboard: X"
```bash
bash skills/clipboard-manager-1.0.0/scripts/clipboard.sh set "<text>"
```

### Show History
When user says: "clipboard history", "show copied items"
```bash
bash skills/clipboard-manager-1.0.0/scripts/clipboard.sh history [--limit 10]
```

### Search History
When user says: "find in clipboard history: X"
```bash
bash skills/clipboard-manager-1.0.0/scripts/clipboard.sh search "<keyword>"
```

### Restore from History
When user says: "restore clipboard item X"
```bash
bash skills/clipboard-manager-1.0.0/scripts/clipboard.sh restore <index>
```

### Clear History
When user says: "clear clipboard history"
```bash
bash skills/clipboard-manager-1.0.0/scripts/clipboard.sh clear
```

## History Format

```markdown
# Clipboard History

## [1] 2026-03-10 10:30:45
```
Pasted content here
```

## [2] 2026-03-10 10:25:12
```
Another copied item
```
```

## Platform Support

| OS | Support |
|----|---------|
| Windows | ✅ (powershell/clip) |
| macOS | ✅ (pbcopy/pbpaste) |
| Linux | ✅ (xclip/xsel) |

## Response Format

When showing clipboard:
```
📋 **Current Clipboard:**
```
Content here...
```
```

When showing history:
```
📋 **Clipboard History** (last 5)

[1] 2026-03-10 10:30 - "Meeting notes..."
[2] 2026-03-10 10:25 - "API endpoint: https://..."
[3] 2026-03-10 10:20 - "console.log('test')"
```

# CtrlZ Skill for OpenClaw

AI Operation Undo System - Revert file modifications, installations, and other changes with one command.

## Overview

CtrlZ is a Git-like undo system that records all "create/update/delete" operations performed by AI in each conversation round, allowing users to revert with one command.

## Features

- ✅ File write/edit/delete undo
- ✅ Directory creation undo
- ✅ Package installation tracking with removal hints
- ✅ Configurable stack size (default: 1, configurable: 3/5)
- ✅ Multiple undo support (e.g., `undo 3`)
- ✅ SQLite-based persistence

## Installation

```bash
# Clone the repository
git clone https://github.com/chrisluo5311/ctrlz-skill.git

# Copy to OpenClaw skills directory
cp -r ctrlz-skill ~/.openclaw/skills/ctrlz

# Restart OpenClaw gateway
openclaw gateway restart
```

## Usage

### User Commands

| Command | Description |
|---------|-------------|
| `/ctrlZ` | Undo the most recent conversation round |
| `/ctrlZ 3` | Undo the last 3 conversation rounds |
| `/ctrlZ list` | List undoable operation records |
| `/ctrlZ stack 5` | Set stack size to 5 undo units |

### Natural Language Triggers

- "undo last step"
- "undo"
- "revert recent changes"
- "ctrl+z"

## How It Works

### 1. Start a Session
```bash
SESSION=$(bash ~/.openclaw/skills/ctrlz/scripts/ctrlz.sh start "Modify config" | jq -r '.session_id')
```

### 2. Record Operations
```bash
bash ~/.openclaw/skills/ctrlz/scripts/ctrlz.sh record $SESSION file_edit "/path/to/file"
```

### 3. Execute Undo
```bash
bash ~/.openclaw/skills/ctrlz/scripts/ctrlz.sh undo
```

## Database

- **Location**: `~/.openclaw/skills/ctrlz/undo.db`
- **Type**: SQLite
- **Tables**:
  - `undo_sessions`: Undo units (conversation rounds)
  - `undo_operations`: Specific operations
  - `settings`: Configuration

## Configuration

```bash
# Set stack size (how many undo units to keep)
bash ~/.openclaw/skills/ctrlz/scripts/ctrlz.sh set-stack 5

# View current stack size
bash ~/.openclaw/skills/ctrlz/scripts/ctrlz.sh get-stack

# View statistics
bash ~/.openclaw/skills/ctrlz/scripts/ctrlz.sh stats

# List undoable operations
bash ~/.openclaw/skills/ctrlz/scripts/ctrlz.sh list
```

## Package Installation Handling

When undoing operations that include package installations, CtrlZ will display:

```
📦 The following package installations cannot be auto-undone:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. npm:lodash
  2. npm:express
  3. pip:requests
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 To remove, manually execute:
   npm uninstall lodash
   npm uninstall express
   pip uninstall requests
```

## Testing

```bash
# Quick demo
bash ~/.openclaw/skills/ctrlz/scripts/demo.sh

# Run all test cases
bash ~/.openclaw/skills/ctrlz/scripts/test_ctrlz.sh
```

## Project Structure

```
ctrlz/
├── SKILL.md              # Skill documentation
├── README.md             # This file
├── TEST_CASES.md         # Test case documentation
└── scripts/
    ├── ctrlz.sh          # Main script
    ├── demo.sh           # Quick demo
    └── test_ctrlz.sh     # Test suite
```

## License

MIT

## Author

Created for OpenClaw AI Assistant

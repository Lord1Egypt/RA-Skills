# Interactive Mode

## Keyboard Shortcuts

**macOS**: Option/Alt key shortcuts require Option-as-Meta in your terminal:
- **iTerm2**: Profiles → Keys → Left/Right Option key → "Esc+"
- **Terminal.app**: Profiles → Keyboard → "Use Option as Meta Key"
- **VS Code**: `"terminal.integrated.macOptionIsMeta": true`

### General Controls

| Shortcut | Description |
|----------|-------------|
| `Ctrl+C` | Cancel current generation |
| `Ctrl+D` | Exit session |
| `Ctrl+G` or `Ctrl+X Ctrl+E` | Open in text editor |
| `Ctrl+L` | Clear prompt input |
| `Ctrl+O` | Toggle transcript viewer |
| `Ctrl+R` | Reverse search command history |
| `Ctrl+V` / `Cmd+V` / `Alt+V` | Paste image from clipboard |
| `Ctrl+B` | Background running tasks |
| `Ctrl+T` | Toggle task list |
| `Esc+Esc` | Rewind or summarize |
| `Shift+Tab` / `Alt+M` | Cycle permission modes |
| `Alt+P` | Switch model |
| `Alt+T` | Toggle extended thinking |
| `Alt+O` | Toggle fast mode |

### Text Editing

| Shortcut | Description |
|----------|-------------|
| `Ctrl+K` | Delete to end of line |
| `Ctrl+U` | Delete to line start |
| `Ctrl+Y` | Paste deleted text |
| `Alt+Y` | Cycle paste history (after Ctrl+Y) |
| `Alt+B` | Move cursor back one word |
| `Alt+F` | Move cursor forward one word |

### Multiline Input

| Method | Shortcut |
|--------|----------|
| Quick escape | `\` + `Enter` |
| macOS default | `Option+Enter` |
| Shift+Enter | Works in iTerm2, WezTerm, Ghostty, Kitty |
| Control sequence | `Ctrl+J` |

For other terminals (VS Code, Alacritty, Warp), run `/terminal-setup`.

### Quick Commands

| Shortcut | Description |
|----------|-------------|
| `/` at start | Command or skill |
| `!` at start | Bash mode — run commands directly |
| `@` | File path autocomplete |

## Vim Editor Mode

Enable via `/config` → Editor mode.

### Mode Switching

| Command | Action |
|---------|--------|
| `Esc` | Enter NORMAL mode |
| `i` / `I` | Insert before cursor / at line start |
| `a` / `A` | Insert after cursor / at line end |
| `o` / `O` | Open line below / above |

### Navigation (NORMAL)

`h/j/k/l` move, `w/e/b` word movement, `0/$` line start/end, `^` first non-blank, `gg/G` document start/end, `f/F/t/T{char}` jump to char.

### Editing (NORMAL)

`x` delete char, `dd/D` delete line, `dw/de/db` delete word, `cc/C` change line, `cw/ce/cb` change word, `yy/Y` yank line, `p/P` paste, `>>/<< ` indent/dedent, `J` join lines, `.` repeat.

## Background Bash Commands

Long-running bash commands and agents can be sent to background with `Ctrl+B`.

## Prompt Suggestions

Grayed-out predictions appear after Claude responds. Toggle via `/config` or `CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=false`.

## Side Questions (`/btw`)

Ask quick questions without adding to conversation context.

## Task List

Toggle with `Ctrl+T`. Share across sessions with `CLAUDE_CODE_TASK_LIST_ID`.

## Command History

Navigate with Up/Down arrows. Reverse search with `Ctrl+R`.

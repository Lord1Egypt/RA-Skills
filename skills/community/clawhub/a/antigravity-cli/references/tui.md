# Interactive TUI

Launch with `agy` in a project directory. Type `/` in the prompt box to open typeahead command selection.

## Slash commands

| Command | Alias | Purpose |
| --- | --- | --- |
| `/add-dir <path>` | | Add a directory path to the active workspace |
| `/agents` | | Open Agent Manager Panel for background subagents |
| `/btw <query>` | | Ask a background side question without interrupting the main conversation |
| `/clear` | | Clear the terminal and reset active conversation contexts |
| `/config` | `/settings` | Open the interactive Settings Editor Overlay |
| `/diff` | | Show unified diff of modified workspace files |
| `/exit` | | Close the TUI session and restore the host shell |
| `/fast` | | Enable fast mode for quick actions |
| `/fork` | `/branch` | Clone the current conversation into a parallel session |
| `/hooks` | | Browse active pre-flight/post-format script hooks |
| `/keybindings` | | Open the keyboard shortcut editor |
| `/logout` | | Disconnect profile and purge auth tokens from secure keyring |
| `/mcp` | | Open the MCP server manager |
| `/model` | | Choose preferred reasoning model; persists across sessions |
| `/open <path>` | | Force a path to open in the default system editor |
| `/permissions` | | Switch global permission presets |
| `/planning` | | Enable multi-turn plan generation mode |
| `/rename <name>` | | Rename the current session thread |
| `/resume` | `/switch`, `/conversation` | Open conversation picker |
| `/rewind` | `/undo` | Roll back conversation history to a previous message |
| `/skills` | | Browse loaded local and global Agent Skills |
| `/statusline` | | Open status bar customization |
| `/tasks` | | Open task manager for background shell execution logs |
| `/title [on/off]` | | Toggle or set terminal window title updates |
| `/usage` | | Open offline developer help in the terminal |

## Essential keybindings

| Key | Action |
| --- | --- |
| `Esc` | Cancel stream, close panels, clear prompt |
| `Ctrl+C` | Terminate CLI session |
| `Ctrl+L` | Clear terminal buffer |
| `Enter` | Submit prompt or confirm selection |
| `Shift+Enter` / `Ctrl+J` | Insert newline without submitting |
| `Ctrl+R` | Open Artifact Review Panel |
| `Ctrl+G` | Edit prompt in `$EDITOR` |
| `Ctrl+V` | Paste media from clipboard |
| `Ctrl+O` | Toggle tool reasoning output |
| `Ctrl+K` | Fast-approve a pending subagent action |
| `Alt+J` | Move to next subagent awaiting approval |
| `Ctrl+A` / `Ctrl+E` | Move cursor to line start/end |
| `Ctrl+Z` / `Ctrl+Shift+Z` | Undo/redo text edit |
| `y` / `n` | Approve/reject tool command or artifact |
| `Shift+A` | Approve all artifacts in review panel |
| `Ctrl+D` | Exit CLI, same as `/exit` |
| `Ctrl+Z` | Suspend CLI to background |

## Interaction tips

- `!` prefix runs terminal commands directly in the prompt.
- `?` shows help and lists slash commands.
- `@` triggers file path autocomplete suggestions.
- `Esc Esc` clears the prompt box when no stream is active.
- `\` at end of line plus `Enter` inserts a clean newline.
- Use `/config` to reduce verbosity when tool call noise is too high.

## Prompt composition

- Press `Enter` to submit the prompt.
- Use `Shift+Enter`, `Ctrl+J`, or `Alt/Option+Enter` to insert newlines without submitting.
- Use trailing `\` plus `Enter` as a terminal-agnostic multiline escape.
- Press `Ctrl+G` from an empty prompt to draft a larger prompt in `$EDITOR`, then save and exit to import it back into the TUI.
- Press `Esc` as the global escape hatch when an agent turn, command, or search path is going the wrong direction.

## Media input

The CLI can accept rich media from the clipboard via `Ctrl+V` or native terminal paste. Use this for screenshots, mockups, recordings, or visual bug reports.

Common supported formats include PNG, JPEG, GIF, WebP, BMP, TIFF, SVG, MP4, MOV, WebM, and AVI.

## Session steering

- Use `/rewind` or `/undo` to return a conversation to a prior point instead of abandoning the session.
- Use `/fork` to branch an experiment from a stable baseline.
- Use `/resume` to switch back to an earlier conversation.
- Use `/agents` to monitor parallel background agents and `Ctrl+K` for fast approval of a waiting subagent action when appropriate.

# Checkpointing

Claude Code automatically tracks file edits, allowing you to rewind to previous states.

## How Checkpoints Work

- Every user prompt creates a new checkpoint
- Checkpoints persist across sessions (accessible in resumed conversations)
- Auto-cleaned along with sessions after 30 days (configurable)
- Only tracks edits made through Claude's file editing tools (Edit, Write, NotebookEdit)

## Rewind and Summarize

Press `Esc+Esc` or use `/rewind` to open the rewind menu.

### Actions

| Action | Effect |
|--------|--------|
| **Restore code and conversation** | Revert both to that point |
| **Restore conversation** | Rewind messages, keep current code |
| **Restore code** | Revert files, keep conversation |
| **Summarize from here** | Compress messages from this point forward |
| **Never mind** | Cancel |

After restoring, the original prompt is restored into the input field for re-sending or editing.

### Restore vs. Summarize

- **Restore**: Reverts state (undoes code, conversation, or both)
- **Summarize**: Compresses messages from selected point forward. No files changed on disk. Original messages preserved in transcript for reference

Summarize is like targeted `/compact` — keeps early context intact, compresses later parts.

To branch off while preserving the original session, use fork: `claude --continue --fork-session`.

## Common Use Cases

- **Exploring alternatives**: Try approaches without losing starting point
- **Recovering from mistakes**: Quickly undo broken changes
- **Iterating on features**: Experiment with variations
- **Freeing context**: Summarize verbose debugging sessions

## Limitations

### Bash Changes Not Tracked

File modifications via bash commands (`rm`, `mv`, `cp`) cannot be undone through rewind.

### External Changes Not Tracked

Manual edits outside Claude Code and edits from concurrent sessions are not captured (unless they modify the same files).

### Not a Replacement for Version Control

Checkpoints are session-level recovery. Use Git for permanent history and collaboration.

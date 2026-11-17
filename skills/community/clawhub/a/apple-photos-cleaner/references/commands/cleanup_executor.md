# Cleanup Executor — `cleanup_executor.py`

Actually move junk photos to trash via AppleScript. Supports old screenshots, screen recordings, burst leftovers, low quality, and duplicates. All items go to Recently Deleted (recoverable for 30 days).

```bash
python3 scripts/cleanup_executor.py --category CATEGORY [--execute --confirm TOKEN] [--human]
```

**Options:**
- `--category` — What to clean up: `old_screenshots`, `all_screenshots`, `screen_recordings`, `burst_leftovers`, `low_quality`, `duplicates`. The screenshot categories are photos only; Photos flags screen recordings the same way, so they're a separate category
- `--screenshot-age N` — Screenshot age in days for old_screenshots (default: 30)
- `--quality-threshold N` — Quality threshold for low_quality (default: 0.3)
- `--limit N` — Maximum items to process (default: 500)
- `--execute` — Actually perform the cleanup (without this, preview only)
- `--confirm TOKEN` — The `confirm_token` from the preview; required with `--execute`
- `--batch-size N` — Items per AppleScript batch (default: 50)
- `--human` — Human-readable summary

**Safety:**
- Without `--execute`, shows preview only (dry run). The preview JSON includes `confirm_token` and `next_command`: the exact command that executes it, using the same interpreter and an absolute script path, so it runs as-is from any directory
- `--execute` needs `--confirm <token>` from that preview. If the token is missing, or the candidates or options changed since the preview, nothing runs: the fresh preview and token are printed and the exit code is 11
- No interactive prompt; piping `yes` does nothing
- Items are moved to Recently Deleted (not permanently deleted)
- 30-day recovery window in Photos.app
- Uses AppleScript through Photos.app (never touches database directly)

**Example Usage:**
```bash
# Preview what would be cleaned
python3 scripts/cleanup_executor.py --category old_screenshots --human

# After the user approves that preview, run its next_command
python3 scripts/cleanup_executor.py --category old_screenshots --screenshot-age 30 \
  --quality-threshold 0.3 --limit 500 --execute --confirm <token>
```

**Usage in Conversation:**

**User:** "Delete my old screenshots"  
**AI:** *Runs cleanup_executor.py --category old_screenshots to show the preview, asks the user, and only after a yes runs the preview's `next_command`*

**User:** "Clean up burst photos"  
**AI:** *Runs cleanup_executor.py --category burst_leftovers --human, shows count and size, asks for confirmation*

**⚠️ AI Tip:** The token is the user's approval of one specific set of items. Only pass `--confirm` after the user has seen that preview and said yes. Never reuse a token across previews, and never execute just to get a token. On exit code 11, show the new preview again.

---

[← All commands](../../SKILL.md#commands)

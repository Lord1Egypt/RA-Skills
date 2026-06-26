# Cache Cleanup

Clean old plugin cache versions and temporary git directories.

> **⚠️ This topic is cleanup-only.**
> If the user says "cache miss", "cache error", "load error", or any plugin diagnostic phrase — **stop and route to [troubleshoot.md](./troubleshoot.md) instead**. cache.md does not diagnose anything; it only deletes stale versions.

## Usage

```bash
scripts/cache-cleanup.sh [--dry-run] [--verbose]
```

- `--dry-run`: Preview deletions without removing
- `--verbose`: Show detailed output

> **Platform**: macOS only. The script uses `stat -f "%B"` (BSD-style birthtime) which is unavailable on Linux. On Linux, `stat -c "%W"` could be substituted but birthtime is not always populated; modification time (`stat -c "%Y"`) is a portable fallback if you adapt the script.

## What It Cleans

- **Old versions**: Keeps only the latest version per plugin in `~/.claude/plugins/cache/<marketplace>/<plugin>/`
- **Temp git dirs**: Removes `temp_git_*` directories in cache root

## When to Use

- After plugin updates (old versions accumulate)
- When disk space is needed
- Periodically as maintenance

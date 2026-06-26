# FAQ

## General

**Q: Will it overwrite my existing MEMORY.md?**
A: Never. The split script only reads it. Your original stays intact.

**Q: Does it send data anywhere?**
A: No. Everything is local Markdown files. No APIs, no cloud, no external services.

**Q: Can I use it with other memory skills?**
A: Yes. It only creates files and cron jobs — no core modifications.

**Q: What if I don't like the topic categories?**
A: Edit them freely. They're just Markdown files. The cron respects your structure.

## Installation

**Q: What if install.sh fails?**
A: Run `bash scripts/verify.sh` to see what's missing. Each step can be done manually — see the templates/ folder.

**Q: Can I run install.sh multiple times?**
A: Yes. It's idempotent — skips anything already set up.

**Q: What OpenClaw versions are supported?**
A: 2026.3.x and later.

## Memory Management

**Q: How big can my memory files get?**
A: The weekly cron trims topic files to ~100 lines each. Daily logs are never trimmed (they're your raw history).

**Q: What if the cron makes a mistake?**
A: Crons only append to topic files, never delete. Worst case: a duplicate entry that gets cleaned up next week.

**Q: Can I disable the crons?**
A: Yes. Run `openclaw cron list` to find the IDs, then `openclaw cron delete <id>`.

## Troubleshooting

**Q: My agent still forgets things after installing.**
A: Check that `memoryFlush.enabled` is `true` in your OpenClaw config. Run `bash scripts/verify.sh`.

**Q: The split script says "No ## headers found".**
A: Your MEMORY.md needs `## Section Name` headers for the splitter to detect topics. Add some headers and try again.

**Q: Crons aren't running.**
A: Check `openclaw cron list` — status should be "ok". If "error", check the cron logs.

# Example: Quarantine Flow

An already-installed skill under `~/.openclaw/skills` produces High findings during an auto-scan.

Expected behavior:
- preserve the report
- move the skill to `~/.openclaw/skills-quarantine/<skillname>-<timestamp>`
- keep the result visible in logs or the journal
- avoid deleting the skill or any unrelated files
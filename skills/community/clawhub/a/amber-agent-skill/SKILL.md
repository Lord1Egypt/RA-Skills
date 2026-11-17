---
name: amber
description: Back up selected local Claude and Codex session stores additively into an explicitly chosen private destination, with a no-write preview.
---
# Amber
Resolve an explicit hosts JSON file and destination with the user. Each host has a safe label and an absolute local source_root. Run scripts/backup.py with --hosts, --destination and --dry-run first; inspect the JSON result. Only run without --dry-run after the user authorizes backup writes.
Sources are read-only. Existing backup files are never replaced or deleted. This preserves first-seen bytes, not later changes to growing session files. For EVERY refresh, choose a new private destination (for example a dated snapshot directory), preview it, and then back up into that fresh directory. Do not reuse a destination and claim growing transcripts were refreshed.
Treat outputs as private. Credential filename exclusions cannot remove secrets embedded in transcript content. Do not publish or commit raw backups. Inspect partial/failed results and stop for user direction rather than claiming success.
Remote SSH transfer is not included: use explicitly mounted local sources or a separately authorized transport.

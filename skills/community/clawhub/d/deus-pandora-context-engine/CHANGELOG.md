# Changelog

## [1.0.0] - 2026-02-19

### Added
- Initial release
- save_context action - saves topic, file, command, pending tasks, notes
- restore_context action - restores project on session start
- switch_project action - switches between projects
- list_projects action - lists all projects with status
- summarize action - generates project summary
- add-task, remove-task, set-status, heartbeat辅助 actions
- Storage in /home/deus/.openclaw/workspace/memory/projects/
- Triggers: session_start, explicit mentions, heartbeat

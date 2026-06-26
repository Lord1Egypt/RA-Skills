# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2026-03-15

### Added
- **SETUP.md** — Comprehensive setup & installation guide (English) covering all tools, API keys, Discord/Telegram bot creation, Google Calendar, SQLite, and troubleshooting
- **SETUP_VI.md** — Hướng dẫn cài đặt đầy đủ (Tiếng Việt) — bản dịch đầy đủ của SETUP.md
- Links to setup guides in README.md and README_VI.md Prerequisites sections
- SETUP.md + SETUP_VI.md listed in File Structure sections of both READMEs

## [1.1.0] - 2026-03-15

### Changed
- **BREAKING:** Replaced local JSON tracker files with SQLite database (`workspace/tracker/educlaw.db`)
- All cron job messages now use SQL queries instead of reading JSON files
- Reports and progress lookups reference SQLite database directly
- Updated guardrails: event deletion check uses `sessions` table `event_id` column
- Updated README.md, README_VI.md, WORKFLOW.md with SQLite documentation

### Added
- `schema.sql` — SQLite schema with 4 tables (sessions, vocabulary, materials, weekly_summaries), indexes, and useful views
- Pre-built SQL views: `v_current_week`, `v_vocab_stats`, `v_words_to_review`, `v_recent_sessions`, `v_materials_unused`
- Inline schema creation fallback in SKILL.md for environments without schema.sql

### Removed
- Local JSON tracker files (`sessions.json`, `vocabulary.json`, `materials.json`, `weekly-summary.json`)
- Google Sheet Integration Workflow section from WORKFLOW.md

## [1.0.0] - 2026-03-15

### Added
- Initial release of EduClaw IELTS Study Planner skill
- 4-step workflow: Schedule Preferences → Research & Plan → Calendar → Documentation
- Bilingual support (English & Vietnamese) with automatic language detection
- Google Calendar integration via gcalcli with unique event descriptions per session
- Dynamic timezone detection (never hardcoded)
- Google Sheet progress tracker (4 tabs: Session Log, Vocabulary Bank, Materials Library, Weekly Summary) — replaced by SQLite in v1.1.0
- Discord notifications for calendar conflicts, study reminders, and progress reports
- 5 cron job templates (daily prep, weekly report, material update, calendar watcher, conflict check)
- 4-month IELTS roadmap template (Band 6.0 → 7.5+) in 4 phases
- Comprehensive guardrails: no auto-scheduling, no auto-conflict resolution, approval required
- Detailed calendar event format with vocabulary, lesson plans, materials, exercises, self-check
- Quality enforcement: 100% unique descriptions across all sessions
- Channel-aware output formatting (Discord, TUI, CLI, Cron)

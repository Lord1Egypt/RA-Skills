# Changelog

All notable changes to ClawFlow will be documented in this file.

## [1.0.1] - 2026-04-24

### Changed
- **Daily-summary section headers aligned with ClawFlow Complete.**
  Sections are now `## Accomplished`, `## Decisions`, `## Open Items`,
  `## For Tomorrow` (were: `## What was done`, `## Documents
  created/updated`, `## Decisions & insights`, `## Open items`,
  `## Priority tomorrow (calendar)`). This makes upgrading to Complete
  safe: tomorrow's morning-brief can still surface yesterday's "Open
  Items" section.
- **Morning-brief lookup is now tolerant** of legacy headers: finds
  `## Open Items`, `## Open items`, or `## Openstaande punten`.
- **Language claim narrowed to reflect reality.** Primary support is
  English + Dutch (canonical greetings + success messages). Other
  languages remain best-effort runtime translation by the LLM.

### Fixed
- Repository layout: reverted an incomplete `src/` refactor back to
  standard root layout (SKILL.md / README.md / INSTALL.md at repo root),
  matching ClawHub's expectations and all installed skill examples.

## [1.0.0] - 2026-03-13

### Added
- Initial release of ClawFlow Free Skill
- Morning brief with agenda, tasks, and daily intention
- Daily summary with end-of-day check-in
- Multi-language support: English + Dutch primary; German, Spanish, French, Italian, Portuguese on a best-effort runtime basis
- Optional Todoist integration
- Optional Google Calendar integration (via gog skill)
- Configuration templates (USER.md, IDENTITY.md, HEARTBEAT.md)
- Comprehensive documentation (README, INSTALL, SKILL)

### Features
- Manual morning brief on demand
- Manual daily summary with interactive check-in
- Personalized greetings with custom emoji
- Yesterday's open items tracking
- Memory file storage for daily summaries

---

**Future versions will include:**
- Bug fixes based on user feedback
- Additional language support
- Enhanced integration options
- Community-requested features

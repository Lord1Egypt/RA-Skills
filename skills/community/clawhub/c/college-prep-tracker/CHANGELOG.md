# Changelog

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this skill adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] — 2026-09-28

Privacy and triggering fixes from ClawHub's security audit.

### Added
- **Privacy and Data Handling** section in SKILL.md and README.md: what's stored, that it stays local and unencrypted, and how to see or delete it
- First-use notice: the assistant tells the user what will be saved, and where, before creating `college-data.json`
- Data-minimization rules: first names only, and no FSA IDs, passwords, tax returns, account numbers, or detailed household finances
- Delete commands for one student ("delete Emma's data") or the whole tracker, with a one-time offer to clear a student's record after decisions are final
- `metadata.openclaw.requires.config` declaring `college-data.json`
- `.clawhubignore` so the `evals/` folder isn't published

### Changed
- Narrowed the `description` so the skill activates when the user wants to set up or update a specific student's tracker, not on any mention of college, the SAT/ACT, FAFSA, or scholarships
- `version` in frontmatter is now unquoted, matching the other skills in the catalog

## [1.0.1] — 2026-05-13

### Changed
- Frontmatter `version` field now quoted as a string per ClawHub CLI requirements
- Added this CHANGELOG.md for consistency with the rest of the published skill catalog

### Notes
- No behavior changes in this release. Purely documentation and metadata cleanup.

## [1.0.0] — 2026-04-12

### Added
- Initial release
- Full college application process tracking for one or more students
- School/college list with application status per school
- Essay tracking (Common App, supplementals, scholarship essays) with versioning notes
- Test score tracking (SAT, ACT, AP, IB, subject tests)
- Recommendation letter tracking with status per writer per school
- Scholarship and financial aid tracking with deadlines
- FAFSA and CSS Profile tracking
- Built-in junior and senior year timeline with milestone reminders
- Per-student profiles for families with more than one applicant
- Persistent storage in `college-data.json`

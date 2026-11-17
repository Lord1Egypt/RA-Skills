# Changelog

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this skill adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] — 2026-09-28

Privacy and triggering fixes from ClawHub's security audit.

### Added
- **Privacy and Data Handling** section in SKILL.md and README.md: what's stored, that it stays local and unencrypted, what's never saved, and how to delete it
- First-use notice: the assistant tells the user what will be saved, and where, before creating `client-data.json`
- Data-minimization rules: business contact details and short conversation summaries only, and no payment card or bank numbers, passwords, tax IDs, or Social Security numbers
- Sharing rules: lookups show only the client asked about, and anything drafted for someone else leaves out revenue and internal notes unless requested
- Delete commands for one client ("delete Riverside Church") or the whole tracker
- `metadata.openclaw.requires.config` declaring `client-data.json`
- `.clawhubignore` so the `evals/` folder isn't published

### Changed
- Narrowed the `description` so the skill activates when the user wants to record or look up something in their tracker, not on any mention of clients, invoices, proposals, or deadlines
- Replaced "detect what the user needs from context" with explicit guidance to ask before saving when intent is unclear
- The no-em-dash rule is now a default style the user can override
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
- Light CRM for freelancers and independent consultants
- Client tracking with project history and communication notes
- Project deliverables, deadlines, and status tracking
- Invoice tracking and follow-up reminders
- Proposal management with stage tracking
- Persistent storage in `client-data.json` for cross-session continuity
- Designed as the organized notebook that keeps a solo operator from dropping balls (not a full accounting suite)

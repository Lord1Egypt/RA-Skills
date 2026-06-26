# Changelog

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this skill adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] — 2026-05-12

### Added
- **Master Volunteer Roster** with skills, blackout dates, preferences, and recent-assignment history (separate from per-event volunteer assignments)
- **Burnout Score** auto-calculated per volunteer (0-5) based on assignment density over the trailing 60 days, with a gentle warning when assigning anyone at score 4+
- **Recurring role scheduling** support for predictable rotations (greeters, nursery, ushers, worship team)
- **Ministry Teams** as a first-class concept: each team has a lead, member roster, and owned events; team-level views aggregate workload and open tasks across the team's events
- **Team handoffs**: clean ownership transitions mid-planning with preserved history
- **Sermon Series tracking** with weekly passages and topics; events can link to a series for themed content, discussion questions, and promo blurbs
- **Liturgical Calendar** awareness with tradition-aware surfacing (general-protestant, anglican, lutheran, catholic, or none); proactive prompts for typical events per season
- Expanded JSON schema to support `ministryTeams`, `volunteerRoster`, `sermonSeries`, and `liturgicalYear` blocks

### Changed
- Frontmatter `version` field now quoted as a string per ClawHub CLI requirements
- Description expanded with new triggers for ministry teams, sermon series, liturgical seasons, and burnout-awareness queries
- "Volunteers" section renamed and split into per-event assignments (existing) and master roster (new) to clarify the distinction

## [1.0.0] — 2026-04-12

### Added
- Initial release
- Event records with status, dates, venue, budget, and notes
- Task checklists with due dates, assignees, and status tracking
- Vendor directory reusable across events
- Per-event volunteer assignments
- Seven built-in planning templates (VBS, Easter/Christmas, retreats, fundraisers, community outreach, weddings, funerals, potlucks)
- Cost and budget tracking with per-event and year-over-year reporting
- Proactive nudges for overdue tasks, upcoming deadlines, and budget thresholds

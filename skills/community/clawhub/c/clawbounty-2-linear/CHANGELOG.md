# Changelog

## [1.0.0] — 2026-03-13

### Added
- Complete `effector.toml` with typed interface (`input: String`, `output: JSON`, `context: GenericAPIKey`)
- Declared permissions aligned with actual behavior (network, env-read, no filesystem)
- Error handling config (retry with exponential backoff)
- Runtime binding for OpenClaw (ClawHub managed tier)
- CI workflow for lint validation on every push
- This changelog

### Fixed
- Typo in Purpose section ("Linera" → "Linear")
- Typo in create command ("No prioirty" → "No priority")
- README link to SKILL.md (was "SKILL.mdd")
- README install command ("instal" → "install")

## [0.1.0] — 2026-02-15

### Added
- Initial SKILL.md with Linear GraphQL commands
- Frontmatter with name, description, emoji, env requirements, install steps
- Full command set: list, search, create, update, comment, cycle
- README with install instructions and reference implementation notes

# Changelog

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this skill adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] — 2026-06-08

### Changed
- Rewrote **Privacy and Data Handling** section in SKILL.md to accurately describe assistant-mediated reads/writes against the local `health-data.json` file and explicitly state that the skill does not direct the assistant to use email, browser, or web-search tools (eliminating any intent-code divergence between claims and behavior)
- Narrowed the activation triggers in the `description` frontmatter to require explicit health-logging context with a named family member or specific health field, and added a "do NOT trigger" guardrail for general health news, casual medication mentions, and symptom-checking requests
- Unquoted the `version` field in frontmatter (matches updated ClawHub CLI semver requirements)

### Added
- **Permissions and Privacy** section in README.md so users see the scope of access (local file only, no external tool calls, refused data categories, no medical advice) before installing
- Sensitive-data guardrails extended: skill now also avoids storing bank/credit/HSA account numbers and verbatim therapy notes

## [1.0.1] — 2026-05-13

### Changed
- Frontmatter `version` field now quoted as a string per ClawHub CLI requirements
- Added this CHANGELOG.md for consistency with the rest of the published skill catalog

### Notes
- No behavior changes in this release. Purely documentation and metadata cleanup.

## [1.0.0] — 2026-04-12

### Added
- Initial release
- Family-wide health record tracking (medications, allergies, doctor visits, immunizations, insurance, prescriptions)
- Per-family-member profiles with full medical history
- Smart reminders for checkups, refills, and immunization schedules
- Allergy tracking with severity flags
- Insurance and provider directory
- Prescription tracking with refill alerts
- Local-only data storage in a JSON file (data never leaves the device)
- Works for a single person or a family of any size

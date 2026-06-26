# Changelog

All notable changes to the Kwanda Cortex Memory skill will be documented in this file.

## [1.1.0] - 2026-03-18

### Changed
- Removed unsupported frontmatter attributes (`version`, `tools`, `user-invocable`) from SKILL.md
- Restructured SKILL.md to follow repo conventions:
  - Added "Core Capabilities" section (replaces flat "Tools" and "Commands" lists)
  - Added "Guardrails and Security" section (consolidates "What NOT to Do" items)
  - Added "Tone and Style" section
  - Added "Privacy & Data Handling" section
  - Renamed "Errors" to "Error Handling" with expanded guidance
- Removed duplicated save/capture guidance (was repeated in both "Mandatory Behavioral Rules" and "Save & Capture")
- Condensed TooToo Bridge section from 28 lines to 15 lines
- Added Support footer to README.md

### Rationale
Alignment with repo conventions established by email-assistant and calendar-assistant skills. No behavioral changes — same agent instructions, reorganized for consistency.

## [1.0.0] - 2026-03-16

### Added
- Initial release
- Comprehensive agent instructions for cortex memory tools (search, save, forget, get)
- Agent command reference (/checkpoint, /sleep, /audit)
- Memory hygiene guidelines (what to save, what not to save)
- Volatile state handling guidance
- Confidence score interpretation
- Memory vs. live state conflict resolution patterns
- Deployment guide with full configuration reference
- CLI command documentation
- Testing checklist
- Troubleshooting guide
- Privacy and data handling documentation

## Description:

Echo Seed is a simple idea capture tool for quick notes, smart categorization, timeline browsing, optional AI analysis, and multi-platform sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zheznanohana](https://clawhub.ai/user/zheznanohana)

### License/Terms of Use:

MIT

## Use Case:

External users and developers can use Echo Seed to run a personal note-capture app that records ideas, links, diary entries, todos, and voice-note placeholders, then searches, exports, analyzes, and optionally syncs them across services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private notes may be exposed when the web service is reachable on a network.

Mitigation: Run the app only on localhost or behind authentication and network controls before storing sensitive notes.

Risk: Note content, URLs, or todo details may be sent to external AI, Notion, or calendar services.

Mitigation: Disable or remove external integrations unless they are explicitly needed, and avoid submitting private or internal URLs.

Risk: Sensitive notes may be used with dependencies that have not been reviewed or updated.

Mitigation: Update and scan dependencies before using the app with private or business-sensitive notes.

Risk: Link analysis may retrieve user-provided URLs and forward extracted content for AI analysis.

Mitigation: Restrict link analysis to trusted public URLs and review the destination services before enabling AI analysis.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zheznanohana/skills/echo-seed)
- [Publisher Profile](https://clawhub.ai/user/zheznanohana)
- [README](README.md)
- [AI Feature Documentation](README-AI.md)
- [Configuration Example](config.example.yaml)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documentation with shell commands, Python scripts, YAML configuration, and JSON/CSV/Markdown app exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs a local Flask and SQLite note app with optional AI analysis, Notion sync, Google Calendar sync, and Telegram queue integration.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

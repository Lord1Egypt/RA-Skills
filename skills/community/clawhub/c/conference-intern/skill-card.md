## Description:

Discover, curate, and register for crypto conference side events via Luma and Google Sheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[surlebeat](https://clawhub.ai/user/surlebeat)

### License/Terms of Use:

MIT-0

## Use Case:

External crypto conference attendees use this skill to discover side events, rank them against personal preferences, and attempt Luma registrations through an agent with browser access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can attempt event registrations and submit personal information to third-party event pages.

Mitigation: Use only trusted event sources, review curated events before registration, and verify consent terms before allowing submissions.

Risk: Optional Luma login stores browser session cookies locally.

Mitigation: Avoid persisted login when not needed, keep the workspace private, and delete luma-session.json after use.

Risk: Security evidence reports weaknesses that could expose users to unintended registrations or phishing pages.

Mitigation: Review source URLs and hostnames carefully before running registration, and prefer manual registration for unfamiliar or suspicious events.

## Reference(s):

- [Conference Intern on ClawHub](https://clawhub.ai/surlebeat/skills/conference-intern)
- [Publisher profile: surlebeat](https://clawhub.ai/user/surlebeat)
- [OpenClaw](https://openclaw.com)
- [Luma](https://lu.ma)
- [jq](https://jqlang.github.io/jq/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON files, local configuration files, and shell command execution results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces per-conference event data, curated schedules, registration status, and prompts for missing required RSVP fields.]

## Skill Version(s):

2.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

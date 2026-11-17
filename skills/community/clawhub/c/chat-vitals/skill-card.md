## Description:

Chat Vitals monitors chat conversation health with real-time insights into quality, promise fulfillment, token efficiency, rework, and plan inflation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carolava](https://clawhub.ai/user/carolava)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI operators use Chat Vitals to monitor local chat sessions, inspect health metrics in a live dashboard, and generate reports with optimization suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local conversation telemetry is generated and retained by the skill.

Mitigation: Install only where local retention is acceptable, avoid sensitive conversations unless retention is approved, and ask the publisher for clear retention and deletion controls before broad use.

Risk: Under-scoped session file handling can read or overwrite JSON files outside the intended data directory.

Mitigation: Treat session IDs as trusted input until validation is added, and require session ID validation plus path confinement before broad deployment.

## Reference(s):

- [Chat Vitals README](artifact/README.md)
- [ClawHub Skill Page](https://clawhub.ai/carolava/skills/chat-vitals)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Terminal text, JSON metrics, and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local conversation telemetry may be retained for reports and dashboards.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

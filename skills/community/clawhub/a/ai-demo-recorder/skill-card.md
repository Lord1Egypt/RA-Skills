## Description:

Record AI-driven browser demos with screencli, producing polished screen recordings with gradient backgrounds, auto-zoom, click highlights, cursor trails, and optional shareable uploads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leshems](https://clawhub.ai/user/leshems)

### License/Terms of Use:

MIT

## Use Case:

Developers and content authors use this skill to have an agent record browser demos, walkthroughs, README media, PR videos, social clips, and before-or-after UI demonstrations from a URL and prompt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recordings and metadata may leave the local machine by default.

Mitigation: Use local-only mode for sensitive or internal applications and review recordings before sharing or uploading.

Risk: Saved authentication state can grant access to private browser sessions.

Mitigation: Treat saved auth files as credentials, limit their use to intended apps, and refresh or remove them when no longer needed.

Risk: Floating npx commands can execute a mutable package version.

Mitigation: Pin and review the screencli version before use in controlled or production workflows.

Risk: Recordings can capture production secrets or sensitive user data.

Mitigation: Avoid entering secrets during recorded flows and prefer test accounts or sanitized environments.

## Reference(s):

- [screencli Website](https://screencli.sh)
- [ClawHub Skill Page](https://clawhub.ai/leshems/skills/ai-demo-recorder)
- [CLI Reference](references/cli-reference.md)
- [Effects Reference](references/effects.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated commands can create local recording files and may upload recordings to screencli.sh unless local-only mode is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

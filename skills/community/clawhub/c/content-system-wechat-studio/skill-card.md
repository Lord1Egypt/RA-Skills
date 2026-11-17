## Description:

Launch a local WeChat article workbench for Markdown import, WeChat HTML preview, theme tuning, image selection, and optional draft push.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abigale-cyber](https://clawhub.ai/user/abigale-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content teams, and publishing operators use WeChat Studio to import Markdown article drafts into a local workbench, preview WeChat-ready HTML, tune theme and image choices, and optionally push reviewed content to a WeChat draft box.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local server exposes file and preview-rendering risks that require review before installation.

Mitigation: Review or patch the local server before use; add API authentication, enforce filesystem containment, and sandbox and sanitize previews.

Risk: Reference URL handling and stored presigned URLs can create network-request or data-exposure risk.

Mitigation: Restrict reference URLs to trusted public HTTPS hosts and avoid storing complete presigned URLs.

Risk: Optional WeChat draft push and SK login workflows involve credentials.

Mitigation: Treat SK and WeChat credentials as secrets and use the workbench only with article content and reference URLs you trust.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abigale-cyber/skills/content-system-wechat-studio)
- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [Banana login portal](https://job.suxi.ai/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, HTML, Files]

**Output Format:** [Markdown guidance with shell commands; local HTML previews and optional WeChat draft output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Starts a local browser workbench; optional draft push depends on existing WeChat publishing credentials.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

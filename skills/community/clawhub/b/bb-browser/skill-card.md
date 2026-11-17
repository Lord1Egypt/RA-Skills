## Description:

Turn any website into a CLI command across 36 platforms and 103 commands, using OpenClaw's browser directly without an extra extension.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yan5xu](https://clawhub.ai/user/yan5xu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run bb-browser site adapters through OpenClaw's browser and extract structured data from social, developer, finance, news, video, and knowledge sites. It is especially useful when a workflow needs one-line CLI access to site data, optional jq filtering, or login-backed browser state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Community website adapters may run with access to data visible in logged-in OpenClaw browser sessions, without documented trusted sources, pinning, or permission limits.

Mitigation: Install only trusted adapter sources, review adapters before use, prefer a separate browser profile for sensitive accounts, and avoid blind community updates for accounts that can post, trade, administer, or expose private data.

## Reference(s):

- [ClawHub bb-browser Skill Page](https://clawhub.ai/yan5xu/skills/bb-browser)
- [ClawHub yan5xu Publisher Profile](https://clawhub.ai/user/yan5xu)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline bash commands, jq examples, and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the bb-browser binary and OpenClaw browser; adapter outputs may depend on site availability and logged-in browser state.]

## Skill Version(s):

0.6.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

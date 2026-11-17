## Description:

In-memory message routing library for multi-channel agent communication with routing rules, filters, transforms, and user-provided platform adapters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and external teams use Channel Bridge to route agent messages across configured channels such as Slack, Discord, Telegram, email, SMS, and Signal, applying filters and transforms before handing messages to user-provided adapters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured filters can fail open and route messages more broadly than intended.

Mitigation: Review every route before deployment, require explicit approval for each destination, and use the skill only where broader-than-expected routing would be acceptable.

Risk: Confidential, regulated, or private channel content could be exposed if routing rules, channel filters, or sender matching are not fixed and reviewed.

Mitigation: Avoid those channels until filters fail closed, advertised channel filters are enforced, sender matching is exact, and destination approval is explicit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/channel-bridge)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with YAML configuration examples and JavaScript code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [In-memory routing; platform adapters are user-provided.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

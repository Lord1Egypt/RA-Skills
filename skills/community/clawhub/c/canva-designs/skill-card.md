## Description:

Create and manage Canva designs, upload assets, export content, and manage brand templates via the Canva Connect API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to automate Canva design workflows from chat, including design management, asset uploads, exports, and brand template operations through ClawLink-managed Canva access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on ClawLink to mediate Canva OAuth access and execute Canva API requests.

Mitigation: Before installation, confirm the user trusts ClawLink and review the Canva permissions granted during OAuth.

Risk: The plugin installation and allowlist configuration persist beyond the current chat.

Mitigation: Tell users when persistent plugin and allowlist changes are made, and verify they still want that setup before installation.

Risk: Create, update, export, upload, delete, and brand-template actions can change Canva account or team content.

Mitigation: Use the documented preview workflow and require explicit user confirmation before write or destructive operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/canva-designs)
- [Canva Developer Documentation](https://www.canva.com/developers/)
- [Canva Connect API](https://www.canva.com/developers/docs/connect/)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=canva-designs)
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the live ClawLink Canva catalog as source of truth; write operations require preview and explicit user confirmation.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

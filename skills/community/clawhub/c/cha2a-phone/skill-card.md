## Description:

Cha2a Phone is an installation and usage guide for CHA2A agent phone capabilities, covering plugin setup, identity configuration, messaging, RCS groups, inbox access, registration, and trust checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install and configure the cha2a-phone plugin, then follow guided references for sending messages, using RCS groups, reading inboxes, registering phone identities, and checking trust levels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned external plugin and phone tools that can send messages, create accounts, upload attachments, or enable auto-reply.

Mitigation: Review the plugin before installation, grant only the specific phone tools needed, and require explicit user confirmation before outbound, registration, group administration, upload, or auto-reply actions.

Risk: The documented demo service relays inbox and message content, and evidence warns against sending sensitive plaintext through it.

Mitigation: Avoid sensitive plaintext on the demo endpoint and prefer a self-hosted or clearly authenticated deployment for real use.

Risk: Group administration and auto-reply can have high-impact side effects if enabled broadly.

Mitigation: Treat admin-key group actions and auto-reply as high-impact actions that require explicit authorization and minimal permissions.

## Reference(s):

- [rcs-server API reference](artifact/references/rcs-api.md)
- [ClawHub skill page](https://clawhub.ai/wwumit/skills/cha2a-phone)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and API endpoint reference.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose plugin installation and configuration steps, permission scoping, and fallback HTTP API calls; does not itself execute phone actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

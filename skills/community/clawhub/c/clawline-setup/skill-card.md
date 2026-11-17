## Description:

ClawLine Setup helps an OpenClaw agent install the ClawLine Channel Plugin, bind a phone UUID, check connection status, and clear pairing through conversational prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qtx0213](https://clawhub.ai/user/qtx0213)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to set up and manage ClawLine mobile app pairing without running command-line steps. It supports conversational installation, UUID binding or replacement, status checks, and disconnecting an existing pairing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation depends on the current external npm package version.

Mitigation: Prefer a pinned and reviewed package version before installing in sensitive environments.

Risk: Normal use can replace an existing phone UUID, clear pairing data, and restart the OpenClaw gateway.

Mitigation: Confirm manually before changing an existing UUID, disconnecting ClawLine, or restarting the gateway.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/qtx0213/skills/clawline-setup)
- [Publisher Profile](https://clawhub.ai/user/qtx0213)
- [ClawLine GitHub Repository](https://github.com/qtx0213/clawline)
- [ClawLine App](https://openclawline.com)
- [npm Package](https://www.npmjs.com/package/@openclawline/clawline-setup)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Conversational Markdown with setup status, command references, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide installation of an OpenClaw plugin, phone UUID binding, gateway restart, status checks, and clearing pairing data.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

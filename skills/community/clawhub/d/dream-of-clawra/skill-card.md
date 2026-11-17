## Description:

Dream Of Clawra helps an OpenClaw agent select fixed Haocun dancing or selfie images from a CDN and send them to messaging channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qidu](https://clawhub.ai/user/qidu)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users can add a persona-oriented selfie and dancing-image capability to an agent. The skill chooses a fixed hosted image based on user context and sends it through a configured messaging channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can persistently rewrite OpenClaw identity and persona files.

Mitigation: Install first in a test agent or back up IDENTITY.md and SOUL.md before running the CLI.

Risk: Broad tool permissions and casual triggers may lead to unintended media sending.

Mitigation: Require explicit confirmation of the selected image, channel, and recipient before sending any outbound message.

Risk: The skill sends hosted image URLs through configured messaging channels.

Mitigation: Verify recipient consent, target identifiers, and OpenClaw gateway settings before enabling automatic or repeated use.

## Reference(s):

- [Dream Of Clawra on ClawHub](https://clawhub.ai/qidu/skills/dream-of-clawra)
- [Publisher profile](https://clawhub.ai/user/qidu)
- [Project repository](https://github.com/qidu/dream-of-clawra)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Hosted image assets](https://cdn.jsdelivr.net/gh/christoagent/haoclaw@main/assets/)
- [Clawra](https://clawra.dev/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, OpenClaw messaging parameters, and selected media URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate outbound media messages through the configured OpenClaw channel and target.]

## Skill Version(s):

1.0.8 (source: server release metadata, manifest.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Clawatar gives an AI agent a 3D VRM avatar viewer with animations, expressions, voice chat, lip sync, and WebSocket control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongping-chen](https://clawhub.ai/user/dongping-chen)

### License/Terms of Use:


## Use Case:

Developers and external users use Clawatar to install and control a browser-based VRM avatar companion for agent visualization, animation, expression control, and optional voice chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run mutable unaudited code from a third-party GitHub repository.

Mitigation: Verify the repository revision and npm dependencies before use, run the viewer in a contained environment, and avoid elevated privileges.

Risk: The local web and WebSocket services may expose avatar controls or voice-chat behavior if reachable beyond localhost.

Mitigation: Keep ports 3000 and 8765 bound to localhost and do not expose them to untrusted networks.

Risk: Voice chat can send spoken content or transcripts to AI or TTS services.

Mitigation: Treat voice input and generated speech text as potentially shared with external AI/TTS services and avoid sensitive content unless the service terms are acceptable.

Risk: The skill notes Mixamo animations with credit and non-commercial requirements.

Mitigation: Confirm asset rights and attribution requirements before commercial deployment.

## Reference(s):

- [Clawatar ClawHub listing](https://clawhub.ai/dongping-chen/skills/clawatar)
- [Clawatar repository referenced by installation instructions](https://github.com/Dongping-Chen/Clawatar.git)
- [Mixamo animation source referenced by skill notes](https://www.mixamo.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent through installing, configuring, launching, and sending WebSocket JSON commands to a local VRM avatar viewer.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

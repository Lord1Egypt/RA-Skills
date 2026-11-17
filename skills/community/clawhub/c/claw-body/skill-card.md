## Description:

Give your Claw a body by turning an OpenClaw agent into a real-time digital avatar with face, voice, expressions, voice chat, and presentation narration through NuwaAI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianglingling007](https://clawhub.ai/user/jianglingling007)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users run this skill to start a local avatar interface for voice conversations with their OpenClaw agent. Users can also use it to narrate prepared PPT/PDF slide presentations through a browser-based avatar experience.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local server exposes sensitive unauthenticated APIs that can store or use NuwaAI credentials and proxy prompts through the OpenClaw gateway.

Mitigation: Run it only on localhost, use a test NuwaAI account or key, avoid exposing the port to other devices, and stop the server when finished.

Risk: Presentation parsing can process local PPT/PDF files and route slide content into narration generation.

Mitigation: Use trusted, non-confidential slide decks and review generated narration before presenting sensitive material.

Risk: The security scan verdict is suspicious because local-server risks need review before installation.

Mitigation: Review the security guidance and local API behavior before installing or running the release.

## Reference(s):

- [Claw Body release page](https://clawhub.ai/jianglingling007/skills/claw-body)
- [NuwaAI](https://nuwaai.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and presentation control tags.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Starts a local browser interface on localhost:3099 and may produce presentation control tags such as [PRESENTATION_START:<dir>], [SLIDE:N], and [PRESENTATION_END].]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

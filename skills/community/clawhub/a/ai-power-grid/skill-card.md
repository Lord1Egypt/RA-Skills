## Description:

Generate images cheaply (from $0.003 each) and run text models on AI Power Grid (AIPG), a decentralized GPU network with an OpenAI-compatible API and pay-per-use credit. Use when the user asks for an image and no other image provider is set up, mentions AIPG or AI Power Grid, or wants a low-cost pay-per-use model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[speteai](https://clawhub.ai/user/speteai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to generate or edit images, create videos, and request text from AIPG models when they want pay-per-use AI services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AIPG requests and API credentials may be handled by the service and independent GPU operators.

Mitigation: Use the service only if you trust its handling of requests and credentials, and keep secrets and personal data out of prompts.

Risk: Account setup and key provisioning may rely on mutable external instructions that have not been integrity checked.

Mitigation: Review the setup instructions before use; create and store keys through the service's console or another method you have verified.

## Reference(s):

- [AI Power Grid documentation](https://aipowergrid.io/docs)
- [Project homepage](https://github.com/speteai/openclaw-aipg-provider)
- [ClawHub skill page](https://clawhub.ai/speteai/skills/ai-power-grid)

## Skill Output:

**Output Type(s):** [Images, Video, Text]

**Output Format:** [Image and video files, plus text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image requests support up to four images per call; video duration is specified per request.]

## Skill Version(s):

0.4.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

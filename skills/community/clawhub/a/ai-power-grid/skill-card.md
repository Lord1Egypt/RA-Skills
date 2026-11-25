## Description:

Generate images cheaply (from $0.003 each) and run text models on AI Power Grid (AIPG), a decentralized GPU network with an OpenAI-compatible API and pay-per-use credit. Use when the user asks for an image and no other image provider is set up, mentions AIPG or AI Power Grid, or wants a low-cost pay-per-use model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[speteai](https://clawhub.ai/user/speteai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw users use this skill to request image, video, and text generation through AI Power Grid, using its OpenClaw provider or OpenAI-compatible API. It also guides account setup, credit-aware use, and safe handling of prompts and API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests go to an external API, and independent operators process submitted content in plain text.

Mitigation: Keep secrets, credentials, and personal data out of prompts; store the API key in the environment or a saved profile rather than chat.

Risk: Paid requests spend account credit, and the security scan was partial because a local reference could not be matched.

Mitigation: Tell the user before the first paid request, check balance and pricing before costly work, and review the unmatched reference before deployment.

## Reference(s):

- [AI Power Grid documentation](https://aipowergrid.io/docs)
- [OpenClaw AIPG provider repository](https://github.com/speteai/openclaw-aipg-provider)
- [AI Power Grid ClawHub release](https://clawhub.ai/speteai/skills/ai-power-grid)

## Skill Output:

**Output Type(s):** [Generated images, Generated video, Text, Shell commands, Configuration guidance]

**Output Format:** [Media files or URLs, text responses, and Markdown instructions with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requests may use account credit; generated images can be saved to a user-visible file path.]

## Skill Version(s):

0.4.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

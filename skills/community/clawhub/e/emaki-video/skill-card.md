## Description:

Generate a short video (Seedance 2.5, Seedance 2.0) or a first-frame image on emaki.ai with the user's own API key. Use when the user asks for a video clip from a text prompt, wants to animate a still (image to video), or needs a quick image to start a clip from, and EMAKI_API_KEY is set.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanshs474](https://clawhub.ai/user/hanshs474)

### License/Terms of Use:

MIT

## Use Case:

Users and agents can create short AI video clips from text prompts, animate a still image, generate a first-frame image, or check an emaki account's remaining credits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The emaki API key is sent to emaki.ai when checking credits or submitting a generation request.

Mitigation: Use the skill only if you trust emaki.ai with the key, keep it in EMAKI_API_KEY, and never print or store it.

Risk: Video and image submissions spend credits, and retries can incur additional charges.

Mitigation: Review the balance, model, settings, and price before approving each run; do not retry a failed or refused run automatically.

## Reference(s):

- [Emaki Seedance 2.5](https://emaki.ai/seedance-2-5)
- [Emaki Seedance 2.0](https://emaki.ai/seedance-2)
- [Emaki pricing](https://emaki.ai/pricing)
- [Emaki API key settings](https://emaki.ai/settings/apikeys)
- [Emaki MCP setup guide](https://emaki.mintlify.app/mcp-server)
- [Emaki MCP repository (referenced by the skill)](https://github.com/hanshs474/emaki-mcp)

## Skill Output:

**Output Type(s):** [Generated media, Text]

**Output Format:** [Video or image URL with a brief status summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video duration, resolution, and aspect ratio follow the approved request.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

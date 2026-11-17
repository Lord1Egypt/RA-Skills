## Description:

Creates videos from a text prompt using HeyGen's Video Agent, with HeyGen handling script, avatar selection, visuals, voiceover, pacing, and captions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelwang11394](https://clawhub.ai/user/michaelwang11394)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and operators use this skill to turn concise briefs into explainer, demo, marketing, or draft videos through HeyGen's Video Agent. It is best suited for prompt-led video creation where exact per-scene, avatar, or voice control is not required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The HEYGEN_API_KEY can grant broad HeyGen account access, including video listing and deletion.

Mitigation: Use a limited or dedicated HeyGen key when possible, scope agent access to the intended account, and require explicit confirmation before deletion.

Risk: Media upload and upload-from-URL workflows can expose unintended files or private/internal URLs.

Mitigation: Confirm each upload, validate file sources before sending them to HeyGen, and avoid private or internal URLs in URL-based uploads.

Risk: Webhook examples are suitable starting points but need hardening before public deployment.

Mitigation: Verify webhook signatures and event origin, reject unexpected payloads, and deploy webhook handlers behind standard production protections.

## Reference(s):

- [HeyGen Video Agent API](https://docs.heygen.com/reference/create-video-with-video-agent)
- [Create Video on ClawHub](https://clawhub.ai/michaelwang11394/skills/create-video)
- [Prompt Optimizer](references/prompt-optimizer.md)
- [Visual Style Library](references/visual-styles.md)
- [Video Agent API](references/video-agent.md)
- [Video Status and Polling](references/video-status.md)
- [Asset Upload and Management](references/assets.md)
- [Webhooks](references/webhooks.md)
- [Video Dimensions and Resolution](references/dimensions.md)
- [HeyGen Quota and Credits](references/quota.md)
- [Video Agent Prompt Examples](references/prompt-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown with optimized prompts, JSON request bodies, and inline shell, TypeScript, or Python examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HEYGEN_API_KEY; may use HeyGen MCP tools when available and direct HeyGen HTTP API calls otherwise.]

## Skill Version(s):

2.23.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

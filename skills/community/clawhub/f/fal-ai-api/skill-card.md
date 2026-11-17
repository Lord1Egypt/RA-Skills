## Description:

Guides agents in using fal.ai models for image, video, and audio tasks through an authenticated Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can ask an agent to run fal.ai models for image generation, video generation, audio processing, upscaling, or transcription, and to manage explicitly approved connections and automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hosted functions, triggers, destinations, or webhooks can create ongoing access or data flows.

Mitigation: Obtain explicit approval for the account, destination host, payload, schedule, and cleanup plan before enabling them.

Risk: Raw API-key use can expose a long-lived credential.

Mitigation: Prefer authenticated CLI access; use raw API keys only when necessary, keep them out of logs and saved files, and rotate any exposed key.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/byungkyu/skills/fal-ai-api)
- [fal.ai documentation](https://fal.ai/docs)
- [fal.ai model gallery](https://fal.ai/models)
- [fal.ai Queue API reference](https://fal.ai/docs/model-endpoints/queue)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Time trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Model responses may include links to generated media; persistent automations require separate approval.]

## Skill Version(s):

1.2.6 (source: ClawHub release metadata; artifact frontmatter lists 1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

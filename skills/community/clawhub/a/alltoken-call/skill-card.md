## Description:

Six slash-style AllToken commands - /alltoken-chat, /alltoken-image, /alltoken-video, /alltoken-search, /alltoken-models, /alltoken-cost - recognized in chat and run via stdlib Python recipes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alltoken-ai](https://clawhub.ai/user/alltoken-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to make direct AllToken chat, image, video, search, model-listing, and cost-estimation calls from an agent session with their own API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send user prompts, search queries, and generation requests to AllToken using the user's API key.

Mitigation: Install only when external AllToken requests are acceptable, require an explicit API key, and avoid sending sensitive prompts or confidential data.

Risk: Loose natural-language trigger matching can make paid external calls when the user did not intend to invoke AllToken.

Mitigation: Prefer explicit slash commands and confirm with the user before running inferred natural-language triggers.

Risk: Recipe examples use predictable shared temporary paths for scripts.

Mitigation: Run recipes from a private temporary directory or a managed script runner rather than fixed shared paths.

## Reference(s):

- [AllToken API documentation](https://alltoken.ai/docs/apis/overview)
- [AllToken homepage](https://alltoken.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Python and shell command recipes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce generated image files, expiring video URLs, model lists, usage summaries, and cost estimates depending on the selected slash command.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

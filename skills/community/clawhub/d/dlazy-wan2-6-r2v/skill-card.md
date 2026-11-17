## Description:

Accurately generate continuous videos based on reference images using Wan 2.6 R2V.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and external users use this skill to invoke dLazy's Wan 2.6 R2V workflow for reference-image-to-video generation from prompts and image inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, parameters, and referenced media are sent to dLazy cloud endpoints for generation.

Mitigation: Pass only media and prompts intended for upload to dLazy, and review the service terms before use.

Risk: The workflow requires a dLazy API key that may be stored in local CLI configuration.

Mitigation: Use a revocable API key, rotate or revoke it when needed, and prefer DLAZY_API_KEY for per-invocation use when appropriate.

Risk: Global CLI installation persists an npm package on the system.

Mitigation: Review the dLazy CLI source before installing globally, or use the pinned npx invocation instead.

Risk: Broad video-generation triggers may activate this skill for generic requests.

Mitigation: Confirm the request is specifically for the dLazy Wan 2.6 R2V workflow before invoking it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dlazyai/skills/dlazy-wan2-6-r2v)
- [dLazy CLI source](https://github.com/dlazyai/cli)
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy homepage](https://dlazy.com)

## Skill Output:

**Output Type(s):** [text, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON results from the dLazy CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI may return hosted result URLs or an asynchronous generateId for later polling.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

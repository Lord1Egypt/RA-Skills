## Description:

Provides access to dLazy's hosted Gemini 3.1 multimodal model for long-context prompting, document parsing, image and video understanding, and structured output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to call dLazy's hosted Gemini 3.1 service for multimodal analysis, long-context reasoning, and structured generation from prompts, images, or videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts and referenced media to dLazy's hosted service for processing.

Mitigation: Only pass prompts and media files that are appropriate to share with the hosted service.

Risk: The skill depends on installing or invoking the third-party @dlazy/cli npm package.

Mitigation: Verify trust in the dlazyai publisher and @dlazy/cli@1.2.0 package before use; prefer npx or an isolated environment when avoiding a persistent global CLI.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dlazyai/skills/dlazy-gemini-3-1)
- [dLazy publisher profile](https://clawhub.ai/user/dlazyai)
- [dLazy CLI source](https://github.com/dlazyai/cli)
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy website](https://dlazy.com)

## Skill Output:

**Output Type(s):** [text, json, code, guidance]

**Output Format:** [JSON response envelope containing generated model outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Async mode can return a generation task identifier for later polling.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Provides access to Alibaba's Qwen 3.8 Max reasoning model for text and image prompts, supporting complex reasoning, code engineering, and long-context analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to submit text or image prompts to the Qwen 3.8 Max model for reasoning, coding, and long-context analysis, then receive generated results through the dLazy service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports incomplete analysis and flags CLI authentication and package use that are not clearly connected to the Qwen purpose; the package itself was not inspected.

Mitigation: Review the pinned @dlazy/cli package and its behavior before installing or invoking it, and confirm that the release matches the intended Qwen use.

Risk: Prompts are sent to dLazy's API, and local media paths may be uploaded to its storage service.

Mitigation: Avoid submitting secrets or sensitive files, and obtain consent before sending private content to the hosted service.

## Reference(s):

- [dLazy CLI repository](https://github.com/dlazy-ai/cli)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service](https://dlazy.com)
- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-qwen3-8-max)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON response containing generated model output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts optional image inputs; asynchronous requests may return a task handle.]

## Skill Version(s):

1.2.37 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

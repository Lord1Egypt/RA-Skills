## Description:

Generate videos from a single first-frame image and a text prompt using Jimeng.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can provide a first-frame image and prompt to request a Jimeng image-to-video generation through the dLazy CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports a mismatch between the stated video-generation purpose and the authentication steps, and scanner coverage is partial.

Mitigation: Review the CLI help and setup flow, and confirm it provides the expected video-generation output before relying on the skill.

## Reference(s):

- [dLazy CLI repository (skill metadata link)](https://github.com/dlazy-ai/cli)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy](https://dlazy.com)

## Skill Output:

**Output Type(s):** [JSON, Media asset URLs, Shell commands, Configuration guidance]

**Output Format:** [JSON response with generation status and output URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation may return a task ID for asynchronous work; duration options are 5 or 10 seconds.]

## Skill Version(s):

1.3.44 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

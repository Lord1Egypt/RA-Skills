## Description:

Video search tool: queries the Pixabay video API by keywords and returns stock video URLs and metadata for footage sourcing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Pixabay stock footage by keyword and retrieve video URLs and metadata for footage sourcing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review noted a mismatch between the video-search purpose and the documented CLI login and authentication commands; using those commands can change local authentication configuration.

Mitigation: Review the CLI behavior before installation, run authentication commands only when you intend to configure an account, and keep API keys out of prompts and logs.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-search-video)
- [dLazy CLI project page](https://github.com/dlazy-ai/cli)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy website](https://dlazy.com)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON containing stock video URLs and metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results for video footage, returned through the dLazy CLI.]

## Skill Version(s):

1.3.45 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

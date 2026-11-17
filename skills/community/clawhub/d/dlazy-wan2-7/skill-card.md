## Description:

通义万相 2.7 视频模型 —— 单一模型支持文生视频、图生视频、首尾帧视频及参考图生成视频。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to generate videos from text prompts, reference media, or specified first and last frames through the dLazy CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The partial scan has medium confidence, with unresolved local references and a reported mismatch between the advertised video-generation purpose and the CLI login behavior it observed.

Mitigation: Before installing, check that the CLI setup supports the advertised video-generation function and review the whitespace finding in the Chinese instructions.

## Reference(s):

- [dLazy CLI repository (linked in skill metadata)](https://github.com/dlazy-ai/cli)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy](https://dlazy.com)

## Skill Output:

**Output Type(s):** [API Calls, Files]

**Output Format:** [JSON result with generated media URLs and task status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Resolution and duration are configurable; tasks can run asynchronously.]

## Skill Version(s):

1.3.40 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

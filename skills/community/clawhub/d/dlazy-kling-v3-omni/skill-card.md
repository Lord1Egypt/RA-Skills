## Description:

使用可灵 (Kling) v3 Omni 全能视频生成模型，支持多模态输入（图片、提示词）生成震撼的动态视频。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to generate videos from text prompts and image or video references, then retrieve or save the resulting assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a benign verdict with medium confidence and notes that the shown login command is not clearly connected to video generation; reference checks were incomplete.

Mitigation: Review the CLI install details and login flow before authenticating.

Risk: The skill sends prompts to a hosted service and uploads local media supplied for generation.

Mitigation: Use only prompts and media that are appropriate to send to the dLazy service.

## Reference(s):

- [dLazy service](https://dlazy.com)
- [dLazy API key instructions](https://dlazy.com/dashboard/organization/api-key)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)

## Skill Output:

**Output Type(s):** [Video assets, JSON result metadata]

**Output Format:** [Hosted video asset URLs and JSON task/result responses; optionally saved video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation may run asynchronously; task IDs can be polled for completion.]

## Skill Version(s):

1.3.43 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

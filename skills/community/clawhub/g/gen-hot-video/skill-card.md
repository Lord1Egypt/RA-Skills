## Description:

Uses the Flyelep hot-video recreation API to generate product videos that follow the visual style of a reference viral video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyelepai](https://clawhub.ai/user/flyelepai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit product and reference videos to Flyelep's API, poll asynchronous generation, and return a generated product video URL in the style of the reference video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private, confidential, personal, regulated, unreleased, or unauthorized videos may be uploaded to long-lived public URLs.

Mitigation: Confirm the user is authorized to upload the media, avoid sensitive or copyrighted material without permission, and prefer user-controlled hosting or expiring private links when available.

Risk: API keys may be exposed through shell commands, terminal history, or logs.

Mitigation: Collect keys at runtime, avoid writing real keys into examples or persistent files, and use secret-handling or environment-variable patterns where the agent environment supports them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flyelepai/skills/gen-hot-video)
- [ClawHub publisher profile](https://clawhub.ai/user/flyelepai)
- [Flyelep open platform](https://www.flyelep.cn/controlboard)
- [Flyelep generateHotVideo API endpoint](https://www.flyelep.cn/prod-api/poster-design/api/v1/aiTool/generateHotVideo)
- [Flyelep queryTaskResult API endpoint](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/queryTaskResult)
- [Flyelep file upload API endpoint](https://www.flyelep.cn/prod-api/poster-design/api/v1/file/upload)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with JSON request bodies and curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asynchronous API workflow that returns a generated video URL after polling; API keys are supplied at runtime.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

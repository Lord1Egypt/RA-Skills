## Description:

使用豆包 Seedream 和 Seedance 通过火山引擎 Ark 生成或编辑图片、创建和管理视频生成任务，并将结果保存到本地。

This skill is ready for commercial/non-commercial use.

## Publisher:

[showtimewalker](https://clawhub.ai/user/showtimewalker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and automation agents use this skill to generate or edit Doubao images and to create, query, download, or delete Doubao video generation tasks with local outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad download and output-path behavior can affect local files or internal URLs if misused.

Mitigation: Set OUTPUT_ROOT to a dedicated folder and avoid passing untrusted URLs or absolute output paths.

Risk: Webhook mode may expose task callback handling if bound beyond localhost.

Mitigation: Keep webhook mode bound to localhost unless the exposure is intentional and understood.

Risk: Delete-task commands perform destructive account actions.

Mitigation: Confirm the task ID and account context before running deletion commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/showtimewalker/skills/doubao-all-in-one)
- [Usage guide](references/usage.md)
- [Seedream prompt guide](references/seedream_prompt_guide.md)
- [Seedance 1.5 Pro prompt guide](references/seedance_1_5_pro_prompt_guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, JSON]

**Output Format:** [Markdown guidance with shell commands, JSON script output, and local image or video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ARK_API_KEY; OUTPUT_ROOT controls the local output location.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

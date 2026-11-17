## Description:

Resizes, scales, and adjusts video resolution and dimensions with GPU-accelerated NVENC encoding through Volcengine LAS, including batch-oriented async submit and poll workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video workflow operators use this skill to resize, upscale, downscale, compress, or re-encode videos through Volcengine LAS while preserving or changing aspect ratio constraints. It guides local or TOS-hosted inputs through credential checks, price estimation, task submission, polling, and result presentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends video inputs, task metadata, and output locations to Volcengine LAS.

Mitigation: Use it only for videos and task data that are approved for Volcengine LAS processing, and confirm credential and TOS bucket scope before execution.

Risk: The environment initialization flow can create a virtual environment and install an SDK wheel from a remote URL.

Mitigation: Run the skill in a restricted workspace and pin or independently verify the SDK package before allowing installation.

Risk: The security summary notes unsafe or mismatched helper scripts.

Mitigation: Review helper scripts before installation or execution, especially result generation, polling, and environment initialization behavior.

## Reference(s):

- [las_video_resize API Reference](artifact/references/api.md)
- [Pricing Information](artifact/references/prices.md)
- [Volcengine LAS Pricing](https://www.volcengine.com/docs/6492/1544808)
- [ClawHub Skill Page](https://clawhub.ai/volcengine-skills/skills/byted-las-video-resize)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include data.json templates, lasutil commands, task IDs, polling status, output video paths, estimated pricing, and local result paths.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

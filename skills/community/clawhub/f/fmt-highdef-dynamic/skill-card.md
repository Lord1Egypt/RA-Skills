## Description:

FMT肠菌移植科普高清动态图生成器（插画版+4K静态图+1080P动态视频+批量模式+风格一致）。生成配套数字手绘插画静态PNG（4K超清），并转化为高清晰度1080P动态视频。风格活泼生动，适合科普教育。触发词：生成FMT动态图 / 生成高清动态 / 插画转高清视频。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to create FMT education assets, including style-anchored 4K static illustrations, 1080P animated videos, page metadata, and generation reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback behavior can run local shell or Python commands using prompt or topic text derived from the user.

Mitigation: Review the skill before installation, sanitize page titles and prompts, avoid shell interpolation, and prefer fixed scripts or structured APIs.

Risk: Generated media files are written under /workspace paths and may affect shared workspace contents.

Mitigation: Run the skill in a dedicated workspace directory and keep all outputs contained to an expected output folder.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zmy1006-sudo/skills/fmt-highdef-dynamic)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with tool calls, shell command examples, JSON metadata, PNG images, and MP4 videos]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a style guide image, per-page static illustrations, animated videos, page metadata, and summary reports under /workspace paths.]

## Skill Version(s):

6.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

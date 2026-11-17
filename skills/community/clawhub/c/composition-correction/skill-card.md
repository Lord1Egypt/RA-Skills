## Description:

墨灵高考作文批改调用 InkCraft API 提交高考作文批改任务并返回结构化点评结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[diyanqi](https://clawhub.ai/user/diyanqi)

### License/Terms of Use:

MIT-0

## Use Case:

Students, educators, and writing coaches use this skill to submit a Chinese gaokao essay prompt and essay text for automated scoring, critique, and rewrite suggestions. The skill is intended for structured feedback workflows backed by InkCraft.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Essay prompts and student writing are sent to InkCraft for correction.

Mitigation: Use the skill only for content that is appropriate to share with InkCraft, and remove unnecessary personal information before submission.

Risk: The API key is sent to a configurable external endpoint.

Mitigation: Protect INKCRAFT_API_KEY and keep INKCRAFT_BASE_URL on the official HTTPS host unless a trusted alternate deployment is required.

Risk: Automated essay feedback may be incomplete or unsuitable as the only assessment source.

Mitigation: Have an educator or qualified reviewer check scoring, critique, and rewrite suggestions before using them for high-stakes decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diyanqi/skills/composition-correction)
- [Publisher profile](https://clawhub.ai/user/diyanqi)
- [InkCraft homepage](https://www.inkcraft.cn)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown response with structured correction sections, troubleshooting guidance, and a detail link when available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires originalText, essayText, curl, and INKCRAFT_API_KEY; may use INKCRAFT_BASE_URL when configured.]

## Skill Version(s):

1.0.0 (source: release evidence, OpenClaw metadata, and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

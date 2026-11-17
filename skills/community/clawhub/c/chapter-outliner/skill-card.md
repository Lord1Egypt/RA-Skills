## Description:

Chapter Outliner generates structured 15-beat writing outlines for novel chapters from project outline, style, character, and chapter inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuzhihui886](https://clawhub.ai/user/yuzhihui886)

### License/Terms of Use:

MIT-0

## Use Case:

External writers and developers use this skill to create detailed chapter planning guides with beat structure, target word allocation, character references, and style notes for downstream novel-writing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled LLM mode can send story outlines, style settings, character profiles, and chapter metadata to DashScope when invoked with DASHSCOPE_API_KEY.

Mitigation: Use the documented local generator for confidential manuscripts, avoid the LLM mode for sensitive projects, and obtain clear user consent before enabling remote generation.

Risk: Dependencies are listed without pinned versions.

Mitigation: Pin and review dependencies before production or organizational deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuzhihui886/skills/chapter-outliner)
- [DashScope Chat Completions Endpoint](https://coding.dashscope.aliyuncs.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown chapter outline or JSON-derived Markdown from CLI execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write an outline file when an output path is provided; the LLM mode requires DASHSCOPE_API_KEY.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

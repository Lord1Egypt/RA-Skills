## Description:

Generates a structured annual work-summary PowerPoint from user-provided accomplishments, highlights, and next-year plans, then shares the .pptx through Feishu or a download link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lixiaojie-1012](https://clawhub.ai/user/lixiaojie-1012)

### License/Terms of Use:


## Use Case:

Employees and professionals use this skill to turn annual achievements, work highlights, and next-year plans into a 6-8 page work-summary PPT for year-end reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated PPT files may contain sensitive work-summary information and are uploaded to an unspecified CDN before being shared by link.

Mitigation: Use only approved data and delivery paths, avoid secrets or highly confidential company information, and prefer a local-only or user-confirmed upload flow.

Risk: The skill asks the agent to generate and run Node.js code and install pptxgenjs if it is missing.

Mitigation: Review generated scripts before execution and install dependencies only from approved sources or a pinned, trusted package setup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lixiaojie-1012/skills/ai-ppt-maker)
- [ClawHub publisher profile](https://clawhub.ai/user/lixiaojie-1012)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with Node.js code and shell commands, plus a generated .pptx file and download link.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and pptxgenjs; artifact behavior includes uploading generated PPT files to a CDN and sharing a link.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

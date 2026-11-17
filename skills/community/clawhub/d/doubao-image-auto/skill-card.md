## Description:

Automates Doubao AI image creation by controlling an existing browser session or related API workflow to submit prompts, extract generated image URLs, and save images locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangm199](https://clawhub.ai/user/huangm199)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to generate images through Doubao by automating prompt submission, image URL extraction, and local download steps. It is intended for workflows where the user can manage the Doubao account session and review generated outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The no-browser API workflow reuses a saved Doubao session cookie without clear scoping or user control.

Mitigation: Use only with an intended Doubao account session, confirm where the session file is stored, and know how to revoke or refresh the session before running automation.

Risk: The artifact references API scripts that are not included, reducing visibility into exact network behavior and file writes.

Mitigation: Review the actual scripts and output directory behavior before using API mode or enabling automatic downloads.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huangm199/skills/doubao-image-auto)
- [Doubao Image Creation Page](https://www.doubao.com/chat/create-image)
- [Doubao](https://www.doubao.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript and PowerShell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce image URLs and saved image files when connected to an authenticated Doubao session.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Automates a content matrix workflow that discovers trending topics, summarizes source material, creates original drafts, adapts them for Xiaohongshu and WeChat, and prepares platform publishing outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and marketing teams use this skill to turn one topic or source into platform-specific content for Xiaohongshu and WeChat. It supports trend discovery, summarization, original draft generation, visual-content guidance, publishing preparation, and release reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish to connected social accounts automatically despite settings that imply draft-only or manual control.

Mitigation: Disable schedules and webhooks by default, keep publishing in draft mode where possible, and require human preview and approval before every publish action.

Risk: The workflow requires publishing access to real Xiaohongshu and WeChat accounts.

Mitigation: Install only when that access is intended, pin and verify dependency skills, and store credentials outside plaintext configuration files.

Risk: Generated or adapted posts may create originality, platform-compliance, sensitive-content, or posting-frequency issues.

Mitigation: Run originality checks, sensitive-word review, platform compliance review, and frequency controls before publication.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform-specific drafts, image-generation guidance, publishing commands, draft or published links, and a summary report.]

## Skill Version(s):

1.0.0 (source: release evidence, workflow.json, SKILL.md, README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

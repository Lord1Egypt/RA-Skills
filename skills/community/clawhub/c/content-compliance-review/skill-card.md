## Description:

Reviews Chinese social-media drafts for prohibited and sensitive terms across seven platforms, with severity-ranked findings, suggested rewrites, and a pre-publication checklist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guipi888](https://clawhub.ai/user/guipi888)

### License/Terms of Use:

MIT

## Use Case:

Social-media creators, editors, and marketing teams use this skill to screen draft copy against general and platform-specific Chinese content rules before publication and to identify wording that needs revision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Drafts may be sent to an external service despite the skill's local-only claims.

Mitigation: Disable the RedFox/API workflow and confirm that no external helper skill runs before reviewing confidential drafts.

Risk: The skill requires a promotional footer in its responses.

Mitigation: Remove the forced promotional footer before using reports or sharing them with others.

Risk: Some suggestions may disguise prohibited claims or off-platform contact instead of resolving the underlying issue.

Mitigation: Reject evasive rewrites and have a human review claims and platform requirements before publication.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/guipi888/skills/content-compliance-review)
- [Review workflow](artifact/references/审核流程.md)
- [Prohibited-word library index](artifact/references/违禁词库.md)
- [WeChat public-account operating guidance](artifact/references/微信公众号和服务号推荐运营规范.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown review report with severity-ranked findings, suggested wording, and a checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes platform-specific checks and optional local prohibited-word scan results.]

## Skill Version(s):

1.1.1 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

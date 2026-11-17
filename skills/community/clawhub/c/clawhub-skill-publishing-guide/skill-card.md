## Description:

A Chinese-language guide that helps developers publish ClawHub Skills, make them searchable after release, and avoid security scan issues that can hide a release.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tudoubudou](https://clawhub.ai/user/tudoubudou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers publishing or updating ClawHub Skills use this guide to prepare required metadata, declare environment variables, accept developer terms, publish through the ClawHub CLI or curl, and verify release visibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on generic publish or update requests because it declares broad triggers such as 发布 and 更新.

Mitigation: Confirm the user is asking about ClawHub skill publishing before applying the guide.

Risk: The curl publishing example reads the local ClawHub token and publishes to the user's account.

Mitigation: Review the developer terms, token source, request payload, and target account before running the example command.

Risk: The guide is written mostly in Chinese, which may make important publishing and security details unclear to non-Chinese readers.

Mitigation: Translate or review the guidance before using it in a release workflow.

## Reference(s):

- [ClawHub Skill page](https://clawhub.ai/tudoubudou/skills/clawhub-skill-publishing-guide)
- [ClawHub publishing API endpoint](https://clawhub.ai/api/v1/skills)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline YAML, Python, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language publishing checklist and troubleshooting guide]

## Skill Version(s):

1.2.1 (source: server release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

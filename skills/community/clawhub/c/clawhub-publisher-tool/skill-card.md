## Description:

一键发布技能到 ClawHub 平台，自动完成登录、版本更新、发布全流程。

This skill is ready for commercial/non-commercial use.

## Publisher:

[romicboy](https://clawhub.ai/user/romicboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to prepare and publish local ClawHub skills, keep version metadata aligned, authenticate with ClawHub, and run release commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles publishing credentials and may expose tokens if users paste real tokens into command lines or logs.

Mitigation: Require explicit account confirmation before use and avoid placing real tokens in commands, transcripts, or logs.

Risk: The skill can release ClawHub skills and suggests running a project-local publish.sh script.

Mitigation: Confirm the exact skill, version, changelog, and account before publishing; inspect and trust any target repository publish.sh before running it.

## Reference(s):

- [ClawHub发布助手 Skill Page](https://clawhub.ai/romicboy/skills/clawhub-publisher-tool)
- [ClawHub Publisher Tool Homepage](https://clawhub.ai/skills/clawhub-publisher-tool)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with shell command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes release checks for package.json, SKILL.md metadata.version, and the publish command version.]

## Skill Version(s):

1.0.3 (source: SKILL.md metadata.version, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

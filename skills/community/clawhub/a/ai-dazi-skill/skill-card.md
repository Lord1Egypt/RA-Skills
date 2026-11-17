## Description:

AI搭子匹配平台 generates local user profiles and matching tags from user-provided AI usage data such as token usage, model preferences, tool calls, and installed skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dory123456](https://clawhub.ai/user/dory123456)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to save user-provided AI usage metrics locally, generate a profile JSON, and display player level, skill tags, AI style, activity score, and matching tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill profiles and stores AI usage metadata locally.

Mitigation: Install only when users are comfortable with local profiling, and review profile contents before sharing them outside the local environment.

Risk: Security evidence reports a path-validation bug that can write JSON files outside the intended data folder.

Mitigation: Validate the save command's date field strictly, for example as YYYY-MM-DD, before accepting or running user-provided JSON.

Risk: Broad trigger wording could collect or refresh profile data before the user fully intends it.

Mitigation: Require explicit user confirmation before collecting usage metadata or generating a profile.

## Reference(s):

- [AI搭子 Skill - 数据格式参考](references/data-formats.md)
- [AI搭子 Skill - 开发与使用指南](references/guide.md)
- [ClawHub Skill Page](https://clawhub.ai/dory123456/skills/ai-dazi-skill)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance, shell commands, and JSON profile files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Profile output is generated from locally stored, user-provided AI usage metadata.]

## Skill Version(s):

2.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

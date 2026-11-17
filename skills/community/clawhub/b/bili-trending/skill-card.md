## Description:

获取B站Top20榜单，提取标题、摘要和链接。

This skill is ready for commercial/non-commercial use.

## Publisher:

[raise7727](https://clawhub.ai/user/raise7727)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve the current Bilibili Top 20 ranking and return each video's title, short description, and link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local script launcher may expose command-execution risk when installed under an attacker-controlled path or a path containing unusual shell characters.

Mitigation: Install only from trusted package sources, avoid attacker-controlled install paths, and replace shell-form execution with shell-free process execution before treating the skill as low risk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raise7727/skills/bili-trending)
- [Bilibili ranking API endpoint](https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to 20 Bilibili ranking entries with title, summary, and video URL; network access to Bilibili is required.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

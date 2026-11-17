## Description:

Helps agents send separate collapsible progress cards and streaming answer cards to Feishu conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingyu9495-source](https://clawhub.ai/user/lingyu9495-source)

### License/Terms of Use:

MIT-0

## Use Case:

Developers integrating agents with Feishu can publish progress and final answers in separate cards and update answer cards as text arrives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing full reasoning, tool logs, or conversation content to Feishu may expose secrets or sensitive data.

Mitigation: Send only short, sanitized progress summaries with consent; never publish raw reasoning, full tool logs, credentials, private file excerpts, or sensitive operational data.

Risk: Feishu bot messaging and card permissions can publish content to external conversations.

Mitigation: Grant only the needed permissions and confirm the intended recipient before enabling card or message sending.

## Reference(s):

- [ClawHub release: feishu-interaction-kit](https://clawhub.ai/lingyu9495-source/skills/feishu-interaction-kit)
- [Feishu developer platform](https://open.feishu.cn/app)
- [Integration examples](references/接入示例.md)
- [Permissions and configuration](references/权限与配置清单.md)
- [Error code reference](references/错误码对照表.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The supplied CLI can return one-line JSON status for Feishu card operations.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

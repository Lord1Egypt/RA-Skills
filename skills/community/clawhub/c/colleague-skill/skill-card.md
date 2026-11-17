## Description:

Distills a colleague into an AI Skill by collecting approved workplace materials and generating Work Skill and Persona files that can evolve over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[titanwings](https://clawhub.ai/user/titanwings)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, developers, and team operators use this skill to preserve and reuse a colleague's work context, communication style, and project knowledge from authorized source materials. It produces generated colleague skills with work guidance, persona behavior, metadata, and versioned updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can collect private workplace messages or broad workspace data without appropriate consent.

Mitigation: Use it only with clear organizational authorization and consent for every person and data source involved.

Risk: Browser-session reuse, app tokens, and MCP-based collection can expose valuable credentials or privileged content.

Mitigation: Use dedicated least-privilege apps or tokens, avoid private chats and browser-profile reuse unless explicitly permitted, and do not use the unpinned MCP path with valuable credentials.

Risk: Generated colleague skills can persist raw knowledge and persona instructions with weak safeguards.

Mitigation: Keep generated knowledge out of synced or shared folders and review generated skills before loading or distributing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/titanwings/skills/colleague-skill)
- [README_EN.md](artifact/README_EN.md)
- [INSTALL.md](artifact/INSTALL.md)
- [AgentSkills Standard](https://agentskills.io)
- [Feishu Open Platform API](https://open.feishu.cn/open-apis)
- [Slack App Configuration](https://api.slack.com/apps)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON metadata, generated skill files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated outputs may include persistent persona and work-context instructions and should be reviewed before loading.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

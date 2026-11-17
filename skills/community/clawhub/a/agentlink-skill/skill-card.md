## Description:

AgentLink Skill provides cloud browser automation, Windows desktop control, shell and Python execution, file, process, and registry operations, and configuration guidance through China Mobile AgentLink sandboxes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sbteng](https://clawhub.ai/user/sbteng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to operate isolated browser and Windows desktop sandboxes for web interaction, scraping, testing, RPA, and command execution. It is intended for tasks where a configured AGENTLINK_API_KEY can be used to create and control cloud sandboxes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can issue broad browser, Windows desktop, command, file, process, registry, and low-level tool actions in cloud sandboxes.

Mitigation: Review before installing, prefer wrapped SDK APIs, and require explicit user approval before logins, package installs, file deletion, process killing, registry edits, or other destructive sandbox actions.

Risk: The skill requires an AGENTLINK_API_KEY that is exposed to the AgentLink SDK at runtime.

Mitigation: Use only API keys acceptable for this integration, configure them through managed environment injection where possible, and avoid placing long-lived secrets in project files.

## Reference(s):

- [AgentLink Product Page](https://ecloud.10086.cn/portal/product/AgentLink)
- [AgentLink Product Docs](https://ecloud.10086.cn/op-help-center/doc/category/1501)
- [AgentLink Console](https://console.ecloud.10086.cn/api/page/AgentLink/web/agentlink/console/#/overview)
- [ClawHub Skill Page](https://clawhub.ai/sbteng/skills/agentlink-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Python, PowerShell, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference generated screenshots, accessibility-tree text, command results, or sandbox file paths when the AgentLink SDK is used.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and pyproject.toml report 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

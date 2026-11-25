## Description:

使用随 Skill 提供的受限 CLI 连接用户已安装并运行的 Easy WebBridge，通过 browserId 读取与交互；复杂能力请使用官方完整运行时。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers and AI agents use this lightweight CLI to inspect and interact with pages in a user-selected, already connected browser for tasks such as web research and form workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks this release suspicious with medium confidence because it found an undeclared tool scope and could only partially inspect a referenced script.

Mitigation: Inspect the bundled CLI before installation and confirm what environment and network access the host will grant.

## Reference(s):

- [Easy WebBridge API reference](references/api.md)
- [Official Easy WebBridge project](https://github.com/aiispower/easy-webbridge)
- [ClawHub release](https://clawhub.ai/xxjrq/skills/easy-webbridge-browser)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Screenshots, PDF files]

**Output Format:** [Markdown summaries and reports, with screenshots or PDF exports when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results reflect the selected browser's current page and session.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

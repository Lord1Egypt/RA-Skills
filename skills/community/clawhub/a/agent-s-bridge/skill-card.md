## Description:

Agent S Bridge lets DeepSeek TUI launch Agent-S to control browser and desktop GUI workflows from natural-language commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangxianzhan](https://clawhub.ai/user/huangxianzhan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to route natural-language desktop and browser automation requests from DeepSeek TUI to Agent-S. It is intended for controlled GUI automation tasks that may span browsers, editors, file managers, and other desktop applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can hand off broad desktop-control tasks that may affect files, applications, browser sessions, and other local resources.

Mitigation: Run it only in a sandbox, VM, or low-privilege account with a test browser profile and no access to production systems.

Risk: The documented browser mode is not technically enforced as browser-only containment.

Mitigation: Do not rely on browse mode for isolation; enforce boundaries with the operating system, account permissions, and browser profile separation.

Risk: The bridge depends on an unpinned third-party desktop-control package.

Mitigation: Pin and verify the gui-agents package before use and review updates before deploying them.

Risk: The workflow requires API keys and may run in logged-in or sensitive user environments.

Mitigation: Use test credentials where possible and avoid payment flows, sensitive files, logged-in personal accounts, and production data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huangxianzhan/skills/agent-s-bridge)
- [Publisher Profile](https://clawhub.ai/user/huangxianzhan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs operational guidance for running Agent-S commands and setting required environment variables.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, _meta.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

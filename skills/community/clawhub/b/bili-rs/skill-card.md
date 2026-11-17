## Description:

Development skill for bili-rs, a Rust CLI for Bilibili, covering architecture conventions, API endpoints, commands, authentication, output formatting, and project constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18621063286](https://clawhub.ai/user/18621063286)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when implementing, fixing, or extending the bili-rs Bilibili CLI while preserving its layered Rust architecture, authentication model, API mappings, and output conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents commands and flows that can read history or change account state, including posting, deletion, follow, like, coin, and credential-related operations.

Mitigation: Require explicit user intent before implementing or running sensitive account, credential, or write-action flows.

Risk: The skill is specific to the bili-rs Bilibili CLI and may be inappropriate outside that codebase.

Mitigation: Install and use it only when working on the bili-rs Bilibili CLI, and review proposed commands before execution.

## Reference(s):

- [bili-rs Skill Page](https://clawhub.ai/18621063286/skills/bili-rs)
- [Bilibili API Endpoints & Payloads](references/api.md)
- [bili-rs CLI Commands Reference](references/commands.md)
- [Bilibili API Base URL](https://api.bilibili.com)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Rust code snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project-specific guidance for the bili-rs CLI, including sensitive authentication and account-action constraints.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

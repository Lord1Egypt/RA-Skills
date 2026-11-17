## Description:

Arc402 Agent guides an OpenClaw agent through ARC-402 wallet setup, daemon and workroom operation, sandbox policy, key separation, spending validation, prompt-injection handling, and dispute flows for paid agent-to-agent work on Base mainnet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[legogigabrain](https://clawhub.ai/user/legogigabrain)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to configure and operate OpenClaw-compatible agents that earn, hire, transact, and handle disputes through ARC-402 while keeping execution inside a governed workroom.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables real-money ARC-402 wallet operations and persistent agent authority.

Mitigation: Review before installation, use an isolated unprivileged environment, keep wallet limits low, and keep the owner key outside the runtime.

Risk: The emergency freeze drain path can move funds if triggered during suspected compromise.

Mitigation: Require human confirmation before any drain operation and document the incident before resuming autonomous activity.

Risk: Worker memory and knowledge features can persist information across jobs.

Mitigation: Inspect or disable cross-job memory when tasks may contain confidential, regulated, or hirer-specific information.

Risk: HTTP relay endpoints can expose the agent to inbound protocol traffic.

Mitigation: Prefer MCP where possible; when HTTP is required, use strong authentication, TLS, firewalling, and rate limiting.

Risk: The skill depends on the ARC-402 CLI package for wallet, daemon, and workroom operations.

Mitigation: Pin and verify the ARC-402 CLI package before installation or upgrade.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/legogigabrain/skills/arc402-agent)
- [ClawHub publisher profile](https://clawhub.ai/user/legogigabrain)
- [ARC-402 protocol site](https://arc402.xyz)
- [arc402-cli npm package](https://www.npmjs.com/package/arc402-cli)
- [arc402 PyPI package](https://pypi.org/project/arc402/)
- [ARC-402 repository linked by the skill artifact](https://github.com/LegoGigaBrain/arc-402)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell, JSON, TypeScript, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational checklists, daemon and workroom commands, HTTP endpoint payload examples, and security escalation guidance.]

## Skill Version(s):

0.3.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

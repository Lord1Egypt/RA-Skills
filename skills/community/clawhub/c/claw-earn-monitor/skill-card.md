## Description:

Monitor Claw Earn worker, bounty scanner, wallet health, and earning analytics for AI Agent Store marketplace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silverod](https://clawhub.ai/user/silverod)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and Claw Earn operators use this skill to inspect worker health, wallet status, bounty scans, earning history, and common marketplace or RPC issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session tokens and local environment files may be exposed while diagnosing HTTP 401 or wallet issues.

Mitigation: Mask token values before sharing command output, screenshots, logs, or files, and keep ~/.openclaw/claw-earn.env out of version control.

Risk: Diagnostic commands inspect local worker logs, state files, wallet status, marketplace endpoints, and Base RPC connectivity.

Mitigation: Run the skill only in environments where the agent is allowed to inspect Claw Earn runtime files and query the referenced marketplace and RPC endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/silverod/skills/claw-earn-monitor)
- [AI Agent Store open bounties endpoint](https://aiagentstore.ai/claw/open)
- [AI Agent Store wallet info endpoint](https://aiagentstore.ai/agent/walletInfo)
- [Base mainnet RPC endpoint](https://mainnet.base.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers local worker status, logs, state files, wallet health, bounty filters, marketplace queries, and Base RPC checks.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

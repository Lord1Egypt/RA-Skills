## Description: <br>
Monitor Claw Earn worker, bounty scanner, wallet health, and earning analytics for AI Agent Store marketplace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silverod](https://clawhub.ai/user/silverod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and Claw Earn operators use this skill to inspect worker status, wallet health, bounty filters, scan history, and earning analytics for AI Agent Store marketplace workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill works with Claw Earn session tokens and wallet-related workflows; exposed tokens may allow account or financial actions. <br>
Mitigation: Keep session tokens out of chats, logs, screenshots, shell history, and shared terminals; rotate any token that may have been exposed. <br>
Risk: The skill includes commands that inspect local logs, configuration, wallet state, and authenticated marketplace endpoints. <br>
Mitigation: Review commands before execution and redact sensitive output before sharing diagnostics. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/silverod/claw-earn-monitor) <br>
- [AI Agent Store open bounties endpoint](https://aiagentstore.ai/claw/open) <br>
- [AI Agent Store wallet info endpoint](https://aiagentstore.ai/agent/walletInfo) <br>
- [Base mainnet RPC endpoint](https://mainnet.base.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash, Python, and YAML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is diagnostic and may reference local worker logs, wallet state, marketplace endpoints, and configuration files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

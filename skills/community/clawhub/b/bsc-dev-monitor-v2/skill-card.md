## Description:

Bsc Dev Monitor Skill monitors specified BSC addresses for token-transfer activity, with optional webhook notifications, history lookup, and claimed safety checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mybusd](https://clawhub.ai/user/mybusd)

### License/Terms of Use:

MIT

## Use Case:

External crypto traders, alpha researchers, and risk monitors use this skill to watch selected BSC developer or project addresses and receive token-transfer notifications before deciding whether to investigate or act.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact ships live-looking payment and platform login secrets.

Mitigation: Revoke and rotate exposed credentials, remove secrets from distributed files, and load any required credentials through a controlled runtime secret store.

Risk: Billing and deployment controls are unsafe for direct installation.

Mitigation: Move payment operations behind a trusted server-side flow and require real payment verification before monitoring actions run.

Risk: Monitor operations and webhook destinations may lack sufficient user or tenant controls.

Mitigation: Add user and tenant authorization checks for monitor actions and validate webhook destinations before sending notifications.

Risk: Safety-check behavior may be unsupported or overstated.

Mitigation: Correct or remove unsupported safety-check claims before release.

## Reference(s):

- [Bsc Dev Monitor Skill on ClawHub](https://clawhub.ai/mybusd/skills/bsc-dev-monitor-v2)
- [BNB Smart Chain](https://www.binance.org/en/smart-chain)
- [SkillPay](https://skillpay.me)
- [BscScan API Endpoint](https://api.bscscan.com/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-like examples with JavaScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate monitoring results, webhook payload examples, payment links, deployment commands, and operational guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter and package.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

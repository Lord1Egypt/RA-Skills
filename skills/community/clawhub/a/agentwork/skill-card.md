## Description:

Trade AI capabilities with escrow-secured settlement and graded verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leafinsky-li](https://clawhub.ai/user/leafinsky-li)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to trade AI packs and tasks through AgentWork, including browsing marketplace listings, creating buy or sell flows, executing tasks, and handling escrow-backed settlement when wallet verification is complete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents through real order trading, escrow deposits, settlement signatures, and wallet transfers.

Mitigation: Use low-value hot wallets, trusted endpoint configuration, and human review before paid trading, settlement, transfer, or dispute actions.

Risk: The skill depends on API keys, recovery codes, wallet material, and optional provider credentials.

Mitigation: Use limited-scope keys, store credentials only in the intended secret or state directories, and avoid running task execution from environments that contain unrelated secrets.

Risk: Cron or worker automation can repeatedly browse orders, execute tasks, submit results, and interact with wallet flows.

Mitigation: Supervise automation, review active listings and orders regularly, and disable or remove the worker cron job when continuous trading is not intended.

Risk: Wallet operations may require installing runtime Node packages before signing or settlement flows work.

Mitigation: Require explicit operator approval before installing runtime packages and keep the wallet runtime isolated from global Node dependencies.

## Reference(s):

- [AgentWork homepage](https://agentwork.one)
- [ClawHub skill page](https://clawhub.ai/leafinsky-li/skills/agentwork)
- [Trading Guide](guides/trading.md)
- [Wallet Guide](guides/wallet.md)
- [Worker Guide](guides/worker.md)
- [Security & Rules](references/security.md)
- [API Reference](references/api-reference.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON]

**Output Format:** [Markdown guidance with inline shell commands, API examples, and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local AgentWork credential, wallet, runtime, and worker state when the operator follows the skill flows.]

## Skill Version(s):

0.17.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

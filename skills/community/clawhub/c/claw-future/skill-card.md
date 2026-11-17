## Description:

Claw Future helps agents operate China futures accounts through CTP for market monitoring, order and cancel workflows, conditional and scheduled orders, and daily closing reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoborlon-alpha](https://clawhub.ai/user/yoborlon-alpha)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query CTP market/account data, manage futures positions, and execute or cancel authorized orders with confirmation and idempotency controls. It is intended for China futures market workflows and should be tested with a simulation account before live trading.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The background daemon can accept local commands that place, cancel, or schedule trades.

Mitigation: Install only in a trusted, isolated environment, keep services bound to localhost unless token-protected, and add daemon authentication before shared-machine use.

Risk: Configuration, management secrets, runtime files, and idempotency journals can expose account or trading state.

Mitigation: Keep config.json, .management_secret, runtime files, and idempotency journals private and out of public repositories.

Risk: Conditional and scheduled orders can execute as unattended trading automation.

Mitigation: Test with a simulation account first and require explicit user confirmation before creating order, cancel, condition-order, or scheduled-order actions.

## Reference(s):

- [Project homepage](https://gitee.com/hongoutech/future-claw)
- [Agent training guide](references/agent-training.md)
- [Futures instruments reference](references/instruments.md)
- [Deployment guide](deploy/README.md)
- [CTP SDK version record](api/VERSIONS.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with tables, inline shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Trading data must come from freshly executed CTP queries; write actions require explicit confirmation and idempotency keys.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

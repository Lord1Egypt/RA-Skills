## Description:

Crypto Trading guides an agent through an autonomous crypto trading loop that gathers market and account data, compares Dify AI and OpenClaw analyses, validates decisions with trading rules, executes market orders, and logs results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuzimaki](https://clawhub.ai/user/wuzimaki)

### License/Terms of Use:


## Use Case:

Developers and trading operators use this skill to coordinate recurring BTC, ETH, and BNB trading decisions with AI market analysis, rule checks, position sizing, order execution, and decision logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes unattended crypto trading that can execute market orders.

Mitigation: Confirm whether the workflow is paper or live trading before use, require explicit order limits and kill switches, and review account permissions before enabling execution.

Risk: The workflow can share account, portfolio, or market context with external AI services.

Mitigation: Review what data is sent to Dify AI and OpenClaw, remove unnecessary sensitive fields, and verify that data handling is acceptable for the intended account.

Risk: Incorrect model analysis, rule validation, or position sizing can cause financial loss.

Mitigation: Run the workflow in paper trading or dry-run mode first, review generated decisions before execution, and enforce conservative position limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuzimaki/skills/crypto-trading)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and command references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce trading decisions, execution notes, validation guidance, and log or configuration updates for an agent-managed workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version text)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

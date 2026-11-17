## Description:

Integrate trading infrastructure (hummingbot/MCP) with paper-first mode and audit logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzfshark](https://clawhub.ai/user/mzfshark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate hummingbot or MCP Axodus Trading with market data, order routing, configuration, paper-mode validation, risk gates, and audit logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Malformed activation metadata could make the skill trigger unpredictably or fail to activate for trading-integration tasks.

Mitigation: Review and replace the malformed triggers entry with explicit activation phrases before installing.

Risk: Live trading paths could place real orders if enabled without deliberate user action and preflight checks.

Mitigation: Keep paper mode as the default and require explicit live-mode selection plus passing risk and connectivity preflight checks.

Risk: Exchange API keys or other secrets could be exposed if stored in the repository or printed in logs.

Mitigation: Use environment or secret-management configuration and avoid committing or logging plaintext credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mzfshark/skills/axodus-trading-integration)

## Skill Output:

**Output Type(s):** [markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown with configuration details and validation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paper mode is the default; live trading requires explicit mode selection and passing preflight checks.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

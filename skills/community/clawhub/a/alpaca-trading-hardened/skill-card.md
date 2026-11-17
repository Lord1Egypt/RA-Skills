## Description:

Execute trades, analyze markets, and manage portfolios using the apcacli command-line tool for Alpaca's Trading API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate Alpaca trading workflows through apcacli, including market data checks, account and portfolio review, order management, and trading command preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect real brokerage accounts through order placement, cancellation, or position closure.

Mitigation: Use paper trading by default and require fresh explicit confirmation before any trade-affecting command.

Risk: Live-trading credentials in general agent sessions can enable unintended or unauthorized account actions.

Mitigation: Keep live credentials out of broad agent environments and prefer isolated sessions with the minimum required access.

Risk: Credential-check commands from the safety report can reveal Alpaca key values in logs or transcripts.

Mitigation: Do not run commands that echo credential values; rotate Alpaca keys if those commands were already used in a logged environment.

Risk: Broad automatic invocation for ordinary market-data questions can escalate from information lookup into trading-capable workflows.

Mitigation: Limit automatic activation and keep market-data questions separate from trade execution unless the user explicitly requests trading operations.

Risk: Unreviewed apcacli versions may change behavior or introduce security issues.

Mitigation: Use a pinned, reviewed apcacli version before deploying the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/snazar-faberlens/skills/alpaca-trading-hardened)
- [apcacli Repository](https://github.com/d-e-s-o/apcacli)
- [Alpaca Documentation](https://docs.alpaca.markets/)
- [Alpaca API Reference](https://docs.alpaca.markets/reference/)
- [Faberlens Safety Evaluation](https://faberlens.ai/explore/alpaca-trading)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose apcacli commands and configuration steps; trade-affecting actions require explicit user review and confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

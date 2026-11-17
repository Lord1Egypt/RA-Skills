## Description:

多维度合约信号分析引擎 — 扫描全市场筛选妖币信号，给出独立多空研判

This skill is ready for commercial/non-commercial use.

## Publisher:

[kc785196](https://clawhub.ai/user/kc785196)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading-system developers use this skill to request cloud-hosted crypto contract signal analysis for a single coin or a market scan. It returns trading-signal style analysis and may provide recharge guidance when the paid remote service reports insufficient balance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides paid crypto-trading signal guidance from a remote service.

Mitigation: Review outputs as informational signals only, validate them against independent sources, and avoid connecting results directly to automated trading without separate risk controls.

Risk: The client sends an identity header and receives recharge links from an unencrypted default API endpoint.

Mitigation: Use only in environments where the remote service and payment destination have been reviewed, and avoid sending sensitive identifiers through the default endpoint.

Risk: The service can charge per call and may return a payment-required recharge flow.

Mitigation: Confirm billing expectations with users before execution and inspect recharge URLs before following them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kc785196/skills/demon-detector)
- [Publisher profile](https://clawhub.ai/user/kc785196)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON examples with shell commands for invoking the client]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime client calls a remote HTTP API and prints JSON analysis or a recharge message.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Queries Bitcoin on-chain structural data, including UTXO, large-output, chip-distribution, holder-structure, and chain-metric data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengcheche-0](https://clawhub.ai/user/fengcheche-0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to query Bitcoin on-chain tables by table name, field, limit, or date and inspect returned chain-structure metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a hardcoded private plain-HTTP API endpoint.

Mitigation: Use it only when the endpoint is trusted, reachable from the user's environment, and protected by appropriate network controls.

Risk: Bitcoin query parameters and returned metrics may be unsuitable for sensitive or decision-critical financial workflows.

Mitigation: Review API responses before relying on them and avoid sensitive financial use unless the endpoint and data quality are independently trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fengcheche-0/skills/btc-data-api)
- [Private BTC API endpoint](http://10.168.1.162:9000)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON]

**Output Format:** [Markdown guidance with command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and access to the configured private HTTP API endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Fx Radar monitors major foreign exchange pairs and retrieves live exchange-rate data from Yahoo Finance, with Frankfurter.app used as a fallback data source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gold3bear](https://clawhub.ai/user/gold3bear)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to query major currency pairs and receive a quick exchange-rate snapshot with threshold-based FX commentary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes live requests to Yahoo Finance and Frankfurter.app, so data may be delayed, unavailable, or different from a user's authoritative market-data source.

Mitigation: Confirm important rates against an authoritative data source before using the output for decisions.

Risk: The printed threshold commentary can be mistaken for financial advice.

Mitigation: Treat the commentary as informational only and require qualified human review for financial decisions.

Risk: Broad exchange-rate trigger terms may activate the skill for loosely related requests.

Mitigation: Review and narrow trigger terms before deployment when precise activation is required.

## Reference(s):

- [Fx Radar ClawHub page](https://clawhub.ai/gold3bear/skills/fx-radar)
- [Yahoo Finance chart endpoint](https://query2.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range=1d)
- [Frankfurter latest rates endpoint](https://api.frankfurter.app/latest?base=USD&symbols={symbols})

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Terminal text with exchange-rate rows and threshold commentary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live public market-data requests; no credential inputs are described.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

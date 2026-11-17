## Description:

Provides Alpha Vantage financial data access for stock quotes, historical K-line data, forex rates, and cryptocurrency exchange rates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kpaxqin](https://clawhub.ai/user/kpaxqin)

### License/Terms of Use:


## Use Case:

Developers and analysts use this skill to query Alpha Vantage market data from an agent workflow, including equities, historical price series, foreign exchange pairs, and cryptocurrency pairs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A personal Alpha Vantage API key may be exposed locally or in logs when configured through command-line usage.

Mitigation: Prefer the demo key or a low-privilege, rotatable key; avoid entering keys in shell commands where history or logs are captured.

Risk: A key that was printed, stored by the tool, or captured in logs may no longer be confidential.

Mitigation: Rotate any exposed Alpha Vantage key before relying on it for ongoing use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kpaxqin/skills/alpha-vantage-api)
- [Alpha Vantage API key registration](https://www.alphavantage.co/support/#api-key)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON objects and concise command-line text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to 30 historical K-line records for daily, weekly, and monthly queries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

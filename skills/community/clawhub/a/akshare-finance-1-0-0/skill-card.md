## Description:

Wraps the AKShare financial data library to help agents fetch public market, macroeconomic, and cryptocurrency data for research and analysis.

This skill is for research and development only.

## Publisher:

[codecanvas762](https://clawhub.ai/user/codecanvas762)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to install AKShare dependencies, call common finance-data APIs, and retrieve public stock, macroeconomic, cryptocurrency, foreign exchange, and metals data for research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reaches external public finance-data services through AKShare, so provider availability, rate limits, or upstream API changes can affect results.

Mitigation: Use a virtual environment, pin dependency versions for reproducible installs, handle returned errors, and verify important data against authoritative sources.

Risk: Returned market data may be delayed, incomplete, or unsuitable for investment decisions.

Mitigation: Use the skill for research and analysis only, cross-check material outputs with multiple sources, and do not treat results as financial advice.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/codecanvas762/skills/akshare-finance-1-0-0)
- [AKShare documentation](https://akshare.akfamily.xyz/)
- [AKShare GitHub repository](https://github.com/akfamily/akshare)
- [Bundled AKShare reference quickstart](artifact/references/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with Python and shell snippets; bundled helper scripts print JSON and AKShare APIs return Pandas DataFrames.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires akshare>=1.12 and pandas>=1.5; returned public market data may be delayed and should not be treated as financial advice.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

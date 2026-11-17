## Description:

Routes Chinese futures and options questions to free AKShare-compatible data sources, recipes, and scripts for live boards, intraday indicators, options Greeks/IV, and RR25 calculations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forevershu](https://clawhub.ai/user/forevershu)

### License/Terms of Use:


## Use Case:

Developers and agents serving Chinese-market finance workflows use this skill to route futures and options requests to AKShare data sources, run documented scripts, and return concise tables or calculations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send requested contracts, symbols, and dates to upstream public market-data providers.

Mitigation: Use it only for queries where those market-data inputs are appropriate to share with AKShare upstream sources.

Risk: Market data, Greeks, indicators, and RR25 outputs may be stale, approximate, or affected by upstream field changes.

Mitigation: Verify calculations and source data before using outputs for trading or other financial decisions.

Risk: Some artifact notes identify MVP limitations, including changing column names, incomplete field mappings, and approximate RR25 selection.

Mitigation: Review output columns and update mappings or recipes when upstream AKShare/Sina/Eastmoney interfaces change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/forevershu/skills/akshare-router-cn)
- [AKShare interface index](artifact/references/INDEX.md)
- [AKShare source notes](artifact/sources/akshare.md)
- [Router map](artifact/maps/router.yml)
- [RR25 method](artifact/methods/rr25.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown guidance with inline shell commands and tabular text output from Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make network requests to public AKShare upstream market-data providers for requested symbols and dates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

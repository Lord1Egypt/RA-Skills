## Description:

Automates Vietnamese stock and market index lookups on FireAnt.vn and returns formatted price, volume, trading, and financial metric data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aholake](https://clawhub.ai/user/aholake)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to check Vietnamese equities and market indices, including current price or index value, volume, trading statistics, and selected financial metrics from FireAnt.vn.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested stock or index symbols are sent to FireAnt.vn through a local headless browser lookup.

Mitigation: Use only when this third-party lookup is acceptable for the requested symbols and market context.

Risk: Returned market data may be incomplete, delayed, or unsuitable as the sole basis for financial decisions.

Mitigation: Treat results as informational and verify investment or trading decisions with authoritative financial sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aholake/skills/fireant-stock)
- [Publisher profile](https://clawhub.ai/user/aholake)
- [FireAnt symbol page pattern](https://fireant.vn/ma-chung-khoan/{SYMBOL})

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-style text with command examples and formatted stock or index metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts one or more Vietnamese stock or index symbols and fetches public FireAnt.vn pages at runtime.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

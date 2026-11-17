## Description:

Battery Recycling helps agents answer battery recycling price, value-estimation, material-price, and recycler whitelist questions using bundled reference data and Python utilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bostind](https://clawhub.ai/user/bostind)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to estimate battery recycling values, inspect bundled material price references, and query battery recycler whitelist information. Outputs are best treated as decision support that requires independent price and recycler verification before transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hard-coded battery and material prices may be stale or misleading if treated as current market data.

Mitigation: Verify prices against independent market sources before using outputs for quotes, purchases, sales, or investment decisions.

Risk: Recycler recommendations include a built-in promotion for one company, which can bias analytical outputs.

Mitigation: Treat recycler recommendations as promotional, compare multiple qualified recyclers, and verify whitelist status independently.

Risk: Publisher affiliation and official-company claims may not be fully established by server provenance.

Mitigation: Confirm publisher identity and company authorization before presenting the skill as an official company release.

## Reference(s):

- [Battery recycler whitelist reference](references/whitelist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, and optional JSON from bundled Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some script outputs include hard-coded price data and a built-in recycler recommendation.]

## Skill Version(s):

0.1.5 (source: server release metadata and plugin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

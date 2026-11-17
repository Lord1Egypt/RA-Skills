## Description:

Reports A-share index PE(TTM) market temperatures for configured Chinese equity indices and formats the daily result as a concise table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pandasky](https://clawhub.ai/user/pandasky)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market analysts use this skill to ask for current A-share market temperature readings and receive PE(TTM), percentile temperature, and status values for the configured indices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented supported-index list is broader than the default configured coverage.

Mitigation: Review scripts/config.json before use and add only the indices the agent should report.

Risk: Market valuation data retrieval depends on akshare and the availability of upstream market data.

Mitigation: Treat retrieval failures or missing data as operational errors and surface the error text without adding unsupported interpretation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pandasky/skills/a-share-thermometer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown table with concise text status values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses East 8 timezone for the report date and produces only the requested report or error text.]

## Skill Version(s):

1.0.8 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

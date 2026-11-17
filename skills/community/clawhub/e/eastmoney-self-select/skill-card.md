## Description:

Manages Eastmoney self-selected stocks by querying, adding, and deleting watchlist entries using Eastmoney account and market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqk000](https://clawhub.ai/user/qqk000)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to inspect and manage an Eastmoney account watchlist through command-line or natural-language requests. It can retrieve watchlist holdings and submit add or delete operations for named stocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change account-linked Eastmoney watchlist data from natural-language input without confirmation.

Mitigation: Review add and delete requests before running them, and only execute commands that intentionally modify the watchlist.

Risk: The skill uses an API key and writes generated CSV and raw JSON files that may contain account-related watchlist data.

Mitigation: Provide MX_APIKEY through a trusted environment and protect generated output files as account-related data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qqk000/skills/eastmoney-self-select)
- [ClawHub publisher profile](https://clawhub.ai/user/qqk000)
- [Eastmoney self-select query endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw/self-select/get)
- [Eastmoney self-select manage endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw/self-select/manage)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration]

**Output Format:** [Console text, CSV files, and raw JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MX_APIKEY. Query results are written under the configured output directory with mx_self_select_ filename prefixes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

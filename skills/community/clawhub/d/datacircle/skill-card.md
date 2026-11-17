## Description:

Every GTM API plan on datacircle.dev, as one file you download and query. LinkedIn profiles, people and company search, find and validate email and phone, company data, jobs and posts, each plan with its price per 1,000, score, rate limits, the fields it returns and its docs. Use it to compare or price a GTM data API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waynehamadi](https://clawhub.ai/user/waynehamadi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and go-to-market teams use this skill to compare pricing, coverage, and limits across GTM data API plans. It downloads the Datacircle catalog and supports querying the data to find plans for a task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloading the catalog to datacircle.json can replace an existing file.

Mitigation: Check for an existing file first, or download to a distinct path and preserve any data that must not be overwritten.

Risk: Catalog contents and listed prices are external and may change.

Mitigation: Treat downloaded data as external input and confirm current pricing with the provider before purchasing.

## Reference(s):

- [Datacircle release on ClawHub](https://clawhub.ai/waynehamadi/skills/datacircle)
- [Datacircle API catalog (JSON)](https://datacircle.dev/datacircle.json)
- [Datacircle documentation](https://datacircle.dev/docs)
- [Datacircle field reference](https://datacircle.dev/fields)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON]

**Output Format:** [Pricing comparisons and query results in text or JSON, with shell commands for downloading and querying the catalog]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the downloaded catalog and selected query criteria]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

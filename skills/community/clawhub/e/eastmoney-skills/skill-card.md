## Description:

Eastmoney Miaoxiang financial skills support financial data lookup, financial information search, stock screening, watchlist management, and simulated portfolio management through MX_APIKEY-authenticated services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqk000](https://clawhub.ai/user/qqk000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill collection to install Eastmoney Miaoxiang financial capabilities for market data retrieval, time-sensitive financial search, stock screening, watchlist operations, and simulated portfolio workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install guide downloads remote ZIP packages without hashes or archive verification.

Mitigation: Install only when the publisher is trusted, and verify archive contents or hashes before unzipping and using the downloaded skills.

Risk: The cleanup step uses a wildcard delete for local skill folders matching mx-skills*.

Mitigation: Do not run the wildcard delete as written; inspect the target directory and remove only the intended old Eastmoney skill folders.

Risk: The skill uses MX_APIKEY and includes watchlist and simulated portfolio operations that can alter user-managed records.

Mitigation: Store the API key securely, avoid logging it, and review write-like watchlist or simulator actions before execution.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/qqk000/skills/eastmoney-skills)
- [Miaoxiang Skills API key page](https://dl.dfcfs.com/m/itc4)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and installation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MX_APIKEY for authenticated skill calls.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Uses AKShare to answer Chinese market-data questions about A-shares, China indexes, open-end mutual funds, macro indicators, macro calendar events, and finance news flashes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickdeep1234](https://clawhub.ai/user/nickdeep1234)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve structured China market data through a fixed AKShare command set and receive concise Chinese summaries for quotes, history, profiles, macro data, calendar events, and finance news.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation is not pinned, so AKShare or transitive dependency changes could alter behavior.

Mitigation: Install and run the skill in an isolated Python environment with reviewed pinned versions of akshare and dependencies.

Risk: The skill contacts AKShare-backed market data sources and may return stale, unavailable, or provider-dependent data.

Mitigation: Treat results as market-data retrieval output, check the returned as_of timestamp, and verify important decisions against authoritative financial sources.

Risk: Responses are designed to be in Chinese, which may not match every user or deployment locale.

Mitigation: Override the response language explicitly when a different language is required.

## Reference(s):

- [AKShare Data Documentation](https://akshare.akfamily.xyz/data/index.html)
- [AKShare Dataset Mapping](references/datasets.md)
- [ClawHub Skill Page](https://clawhub.ai/nickdeep1234/skills/ashare)
- [Publisher Profile](https://clawhub.ai/user/nickdeep1234)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Guidance]

**Output Format:** [Chinese Markdown summary derived from JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled CLI returns JSON envelopes with resolved symbol metadata, columns, rows, row counts, truncation status, and timestamps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

CompanyInformation helps agents query FEEDAX for listed-company news and public-opinion signals, including sentiment, heat score, industry classification, stock identifiers, sources, summaries, and event tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longgggggg](https://clawhub.ai/user/longgggggg)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to monitor company news, identify positive, neutral, or negative public-opinion signals, and export results for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials may be exposed if pasted into chat, stored in readable files, or passed on the command line.

Mitigation: Use a scoped environment variable or secure secret store, avoid command-line API key usage, and do not let the agent read full .env files.

Risk: The security evidence states that this version sends API credentials over unencrypted HTTP.

Mitigation: Do not use this release unless FEEDAX access can be made HTTPS-only.

Risk: CSV and Markdown exports can retain local records of user queries and returned company-news results.

Mitigation: Store exports only where appropriate, review them before sharing, and delete retained reports when they are no longer needed.

## Reference(s):

- [FEEDAX](https://www.feedax.cn)
- [CompanyInformation ClawHub listing](https://clawhub.ai/longgggggg/skills/companyinformation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chat text plus CSV and Markdown files, with optional Python CLI commands and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FEEDAX API access; exported CSV and Markdown reports are retained local query records.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

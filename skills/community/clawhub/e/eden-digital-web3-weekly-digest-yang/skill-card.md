## Description:

Automatically gathers public Web3 market and news data to help produce a Chinese weekly capital markets digest covering fundraising, regulation, public-company digital asset treasury activity, M&A, and RWA project updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baoyangispoor](https://clawhub.ai/user/baoyangispoor)

### License/Terms of Use:

MIT-0

## Use Case:

Editors, analysts, and agents use this skill to assemble a Web3 weekly report from public data sources, then complete marked analysis fields with AI-assisted commentary. It is intended for Chinese-language Web3 capital markets coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch a user-supplied RWA URL and the security evidence notes an under-scoped URL fetch path.

Mitigation: Use --rwa-url only with a verified PANews article URL, and avoid passing arbitrary or untrusted URLs.

Risk: Fetched web content is routed into AI completion and may contain untrusted or misleading text.

Mitigation: Review fetched report text before AI completion and avoid granting the completing AI file, shell, memory, or broad network tools.

Risk: Public market and news sources may be incomplete, unavailable, or changed by their providers.

Mitigation: Cross-check key figures, dates, and URLs against the cited sources before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baoyangispoor/skills/eden-digital-web3-weekly-digest-yang)
- [TechFlow RSS](https://www.techflowpost.com/api/client/common/rss.xml?page=1)
- [Rootdata Fundraising](https://www.rootdata.com/Fundraising)
- [CoinGecko public treasury API](https://api.coingecko.com/api/v3/companies/public_treasury/bitcoin)
- [PANews RWA column](https://www.panewslab.com/en/columns/019888d2-9a04-7e7b-97b5-5a1eac76759a)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown weekly report with inline shell commands and marked fields for AI completion]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches public Web3 data sources and generates a report skeleton before AI-assisted completion.]

## Skill Version(s):

8.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

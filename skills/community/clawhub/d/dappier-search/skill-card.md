## Description:

Enable fast, free real-time web search and access premium data from trusted media brands-news, financial markets, sports, entertainment, weather, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amaan-ai20](https://clawhub.ai/user/amaan-ai20)

### License/Terms of Use:


## Use Case:

Developers and external agent builders use this skill to let agents call Dappier for real-time search, news, stock market, sports, lifestyle, research paper, and residential solar analysis results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-entered queries, ticker searches, research terms, and residential addresses are sent to Dappier.

Mitigation: Avoid submitting secrets, private customer data, account details, or sensitive personal information in skill queries.

Risk: The Stellar AI workflow can include residential address data.

Mitigation: Use it only when a specific address is necessary for the requested solar or roof analysis and the user is comfortable sharing that address with Dappier.

Risk: Real-time search, market, news, sports, lifestyle, and research results may change or be incomplete.

Mitigation: Treat returned content as external Dappier data and verify important financial, legal, medical, safety, or time-sensitive decisions against authoritative sources.

## Reference(s):

- [ClawHub Dappier skill release](https://clawhub.ai/amaan-ai20/skills/dappier-search)
- [Dappier homepage](https://dappier.com)
- [Dappier platform](https://platform.dappier.com)
- [Dappier API keys](https://platform.dappier.com/profile/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-friendly command output and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js with global fetch and a DAPPIER_API_KEY environment variable.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

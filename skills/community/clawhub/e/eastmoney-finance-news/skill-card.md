## Description:

Searches Eastmoney data to retrieve timely financial news, research reports, announcements, and policy analysis for natural-language financial queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yunduanmanbu](https://clawhub.ai/user/yunduanmanbu)

### License/Terms of Use:

MIT-0

## Use Case:

Financial analysts, researchers, and agent users use this skill to query Eastmoney for market news, reports, announcements, policy analysis, and related securities for a natural-language topic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User queries and financial topics are sent to the Eastmoney API.

Mitigation: Do not submit confidential investment research, internal company names, regulated data, or other sensitive prompts unless that disclosure is acceptable.

Risk: The artifact includes an embedded default Eastmoney API key.

Mitigation: Prefer a user-controlled, scoped API key through EASTMONEY_APIKEY and treat the embedded default key as exposed.

Risk: The helper can write query results to local text files in the working directory.

Mitigation: Review output files before sharing or committing them, and avoid saving sensitive query results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yunduanmanbu/skills/eastmoney-finance-news)
- [Eastmoney News Search API Endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search)

## Skill Output:

**Output Type(s):** [text, code, shell commands]

**Output Format:** [Plain text financial-news results with optional local text files; helper code returns parsed JSON responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include titles, related securities, and core article or report content.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

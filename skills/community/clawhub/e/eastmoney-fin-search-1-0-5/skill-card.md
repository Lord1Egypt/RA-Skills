## Description:

Eastmoney Fin Search helps agents retrieve current financial news, research, announcements, policy updates, trading-rule information, event context, and impact analysis from Eastmoney Miaoxiang search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouhuihui008](https://clawhub.ai/user/zhouhuihui008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and financial research users use this skill to give an agent access to up-to-date Eastmoney financial information for questions about stocks, sectors, macro conditions, policies, events, and market-moving developments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial search queries are sent to Eastmoney's API using MX_APIKEY.

Mitigation: Run the skill only in a trusted environment, provide MX_APIKEY through the environment, and avoid including client secrets, private account details, or confidential investment research in queries.

Risk: The skill may retain extracted text and raw JSON result files locally.

Mitigation: Review the configured output directory and apply appropriate access control, retention, and deletion practices for stored search results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhouhuihui008/skills/eastmoney-fin-search-1-0-5)
- [Eastmoney Miaoxiang News Search API Endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration guidance]

**Output Format:** [Plain text summaries, raw JSON results, and terminal-readable output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MX_APIKEY; can save mx_search_<query>.txt and mx_search_<query>.json result files under the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact _meta.json reports 1.0.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Eastmoney Skills helps agents search Eastmoney Miaoxiang financial information for current news, announcements, research reports, policies, trading rules, event details, and impact analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqk000](https://clawhub.ai/user/qqk000)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve current, source-filtered financial news and research through the Eastmoney Miaoxiang API when answering market, security, policy, or event-specific questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial search queries are sent to the documented Eastmoney API.

Mitigation: Avoid including confidential client information, proprietary trading intent, or other sensitive details in queries.

Risk: Search outputs are written as local text and JSON files.

Mitigation: Use a private trusted output directory and avoid shared writable paths.

Risk: Running the skill with unnecessary privileges can increase impact if local paths or dependencies are misused.

Mitigation: Run the skill without elevated privileges.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qqk000/skills/eastmoney-fin-search)
- [Eastmoney Miaoxiang News Search API](https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search)

## Skill Output:

**Output Type(s):** [text, JSON, files]

**Output Format:** [Plain text search results and raw JSON API responses saved as local files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MX_APIKEY and writes query-specific .txt and .json result files to the configured output directory.]

## Skill Version(s):

1.0.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

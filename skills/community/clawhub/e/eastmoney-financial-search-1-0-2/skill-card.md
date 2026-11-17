## Description:

Searches Eastmoney financial information sources for timely news, announcements, research reports, policies, trading rules, event details, and related financial analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and financial-analysis agents use this skill to retrieve current Eastmoney financial search results for securities, sectors, macro topics, policies, announcements, research reports, and market events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions show an echo command for EASTMONEY_APIKEY, which can expose the API key in terminal output, logs, or transcripts.

Mitigation: Verify that EASTMONEY_APIKEY is set without printing its value, keep request headers out of logs, and run the skill only in trusted environments.

Risk: Financial search queries are sent to Eastmoney's external API and may contain confidential personal, business, or trading-strategy information.

Mitigation: Avoid submitting confidential or sensitive query text and review data-handling expectations before using the API.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lean-zhouchao/skills/eastmoney-financial-search-1-0-2)
- [Eastmoney Skills marketplace](https://marketing.dfcfs.com/views/finskillshub/indexuNdYscEA?appfenxiang=1)
- [Eastmoney financial news search API endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API responses and shell or Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the EASTMONEY_APIKEY environment variable and sends the user's financial search query to Eastmoney's API.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact _meta.json lists 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

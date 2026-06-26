## Description: <br>
Access and summarize public Eastmoney market quotes, news, announcements, and industry trends without trading or bulk data extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codenova58](https://clawhub.ai/user/codenova58) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to retrieve and summarize public Eastmoney quote, news, announcement, and sector trend pages for lightweight internal analysis and alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public market data can be time-sensitive or stale if reused after retrieval. <br>
Mitigation: Treat outputs as informational summaries, include retrieval context where useful, and verify current values before relying on them. <br>
Risk: Users may over-apply informational summaries as trading or investment advice. <br>
Mitigation: Keep use limited to public-page summaries and internal analysis; do not use the skill for trading, account access, or investment advice. <br>
Risk: Repeated access to public pages can exceed platform expectations or access limits. <br>
Mitigation: Use lightweight requests, avoid bulk collection, and respect Eastmoney platform access limits. <br>


## Reference(s): <br>
- [Eastmoney Home Page](https://www.eastmoney.com/) <br>
- [Eastmoney Quote Center](https://quote.eastmoney.com/center/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries with extracted links and data fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Informational public-market summaries only; no trading, account access, bulk scraping, or investment advice.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Searches Reddit posts and discussions by keyword through the Clawec API for community sentiment, user-need discovery, and product research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anyunzhong](https://clawhub.ai/user/anyunzhong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and ecommerce researchers use this skill to query public Reddit discussions by keyword, then summarize relevant posts, engagement, and product or user-need signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Reddit search keywords and the Clawec API key to Clawec as part of its disclosed function. <br>
Mitigation: Use only organization-approved search terms and credentials; avoid secrets, private customer data, unreleased product plans, or regulated information unless Clawec has been approved for that data. <br>
Risk: Reddit search results are public discussions and may be anecdotal or context-dependent. <br>
Mitigation: Treat summaries as research signals, not sales data or definitive market conclusions, and review linked discussions before making decisions. <br>


## Reference(s): <br>
- [Reddit search response schema](references/response-schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/anyunzhong/clawec-reddit-search) <br>
- [Clawec API base URL](https://www.clawec.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries, tables, and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Reddit post titles, subreddits, scores, comment counts, links, and concise research observations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

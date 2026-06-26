## Description: <br>
Generates personalized coffee chat playbooks for networking conversations by researching a target contact, company, industry, and recent content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gloriathepenguin](https://clawhub.ai/user/gloriathepenguin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and professionals use this skill to prepare for networking coffee chats. It gathers target, company, industry, and recent-content context, then produces a meeting playbook with profile comparison, questions, talking points, communication tips, and a pre-chat checklist. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect public professional profile data and recent social posts for networking research. <br>
Mitigation: Use it only for contacts and meeting contexts where this research is appropriate, and review generated summaries before relying on them. <br>
Risk: Generated profile data and playbooks may be saved locally under memory/. <br>
Mitigation: Store only necessary personal context and delete saved playbooks or profile data when they are no longer needed. <br>
Risk: Optional Notion export can append researched content to a user-shared Notion page. <br>
Mitigation: Use least-privilege Notion access, share only the intended page with the integration, and avoid exposing real API tokens in shared chats or files. <br>
Risk: Optional X post scraping through Apify depends on external service credentials and scraped content quality. <br>
Mitigation: Use Apify credentials carefully, avoid storing tokens in files, and verify scraped or searched content before using it in a meeting. <br>


## Reference(s): <br>
- [Coffee Chat Skill Page](https://clawhub.ai/gloriathepenguin/coffee-chat) <br>
- [Apify Account Integrations](https://console.apify.com/account/integrations) <br>
- [Notion Integrations](https://www.notion.so/my-integrations) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown playbook with optional shell commands and Notion API payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save playbooks under memory/ and optionally append results to a user-shared Notion page when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

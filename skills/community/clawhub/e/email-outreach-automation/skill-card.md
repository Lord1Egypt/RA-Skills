## Description: <br>
Cold email outreach pipeline with multi-step sequences, reply tracking, bounce handling, and campaign analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mhmalvi](https://clawhub.ai/user/mhmalvi) <br>

### License/Terms of Use: <br>
CC BY-NC-SA 4.0 <br>


## Use Case: <br>
External sales, recruiting, agency, freelance, and founder teams use this skill to run a self-hosted n8n outreach pipeline for prospect import, sequenced follow-up, reply tracking, and campaign reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflows can automatically send cold emails, creating compliance, reputation, and abuse risk if enabled without controls. <br>
Mitigation: Use a dedicated SMTP account, add send limits and campaign approval, enforce unsubscribe and suppression handling, and test with a small non-production list before enabling schedules. <br>
Risk: Webhook controls are weak, including a default secret fallback and an unauthenticated reply webhook. <br>
Mitigation: Remove the default secret fallback, require authentication on both webhooks, and keep OUTREACH_SECRET configured as a deployment secret. <br>
Risk: Prospect and reply data is stored in Google Sheets and may include personal or business contact data. <br>
Mitigation: Use a scoped Google Sheet and least-privilege Google Sheets OAuth2 credentials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mhmalvi/email-outreach-automation) <br>
- [Publisher Profile](https://clawhub.ai/user/mhmalvi) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with n8n workflow JSON files and example shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployable n8n workflow configuration that requires Google Sheets OAuth2, SMTP credentials, OUTREACH_SECRET, and OUTREACH_ADMIN_EMAIL.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

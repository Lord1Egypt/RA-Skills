## Description: <br>
ActiveCampaign API integration with managed OAuth for marketing automation, CRM, contacts, deals, email campaigns, automations, tags, lists, users, accounts, custom fields, notes, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, CRM, and operations teams, plus developers assisting them, use this skill to inspect and manage ActiveCampaign resources through Maton-managed OAuth. It supports contact, deal, list, campaign, automation, tag, account, custom field, note, and webhook workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Maton API key and ActiveCampaign OAuth access can read or manage data in the connected account. <br>
Mitigation: Install only if you trust Maton to proxy ActiveCampaign access, keep MATON_API_KEY in the environment, and specify the intended connection when multiple accounts are available. <br>
Risk: Create, update, and delete calls can change CRM and marketing resources. <br>
Mitigation: Confirm the exact resource, account, and intended effect with the user before every write operation. <br>
Risk: Webhook creation can send ActiveCampaign account event data to an external URL. <br>
Mitigation: Confirm the destination URL, subscribed events, and business intent before creating a webhook. <br>
Risk: User and account management actions can affect shared resources and team access. <br>
Mitigation: Treat user and account changes as administrative actions and require explicit confirmation before modifying them. <br>


## Reference(s): <br>
- [Maton](https://maton.ai) <br>
- [ActiveCampaign API Overview](https://developers.activecampaign.com/reference/overview) <br>
- [ActiveCampaign Developer Portal](https://developers.activecampaign.com/) <br>
- [ActiveCampaign API Base URL](https://developers.activecampaign.com/reference/url) <br>
- [Contacts API](https://developers.activecampaign.com/reference/list-all-contacts) <br>
- [Tags API](https://developers.activecampaign.com/reference/contact-tags) <br>
- [Deals API](https://developers.activecampaign.com/reference/list-all-deals) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTTP, Python, JavaScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY, network access, and explicit user approval before write operations.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

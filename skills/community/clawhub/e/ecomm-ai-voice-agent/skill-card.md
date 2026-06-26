## Description: <br>
Complete AI voice agent system for eCommerce order confirmation, customer support, and outbound campaigns with 12 n8n workflows for Vapi AI voice, Twilio SMS, Shopify/WooCommerce integration, and Google Sheets CRM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mhmalvi](https://clawhub.ai/user/mhmalvi) <br>

### License/Terms of Use: <br>
CC BY-NC-SA 4.0 <br>


## Use Case: <br>
External ecommerce teams and developers use this skill to deploy automated order confirmation, customer support, retry, fallback messaging, status update, CRM logging, reporting, and callback workflows for online stores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Customer-contact and order-update workflows may be invoked through webhooks without visible authentication or signature checks. <br>
Mitigation: Add webhook authentication or signature checks, schema validation, and rate limits before production use. <br>
Risk: Provider tokens and Sheets or CRM credentials can grant access to customer and order records. <br>
Mitigation: Use least-privilege provider tokens, restricted Sheet and CRM access, sandbox credentials first, retention rules, and audit logging. <br>
Risk: Automated calls and messages can contact customers repeatedly or without appropriate consent controls. <br>
Mitigation: Implement opt-in, opt-out, do-not-call controls, retry limits, and manual review for high-value or destructive order changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mhmalvi/ecomm-ai-voice-agent) <br>
- [Publisher profile](https://clawhub.ai/user/mhmalvi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with n8n JSON workflow definitions and environment-variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes 12 n8n workflow definitions and requires provider credentials and environment variables for voice, SMS, messaging, ecommerce, CRM, spreadsheet, AI, and email integrations.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata; artifact frontmatter and _meta.json report 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

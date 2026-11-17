## Description:

Complete AI voice agent system for eCommerce order confirmation, customer support, and outbound campaigns. 12 production-ready n8n workflows with Vapi AI voice, Twilio SMS, Shopify/WooCommerce integration, and Google Sheets CRM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mhmalvi](https://clawhub.ai/user/mhmalvi)

### License/Terms of Use:

CC BY-NC-SA 4.0

## Use Case:

Store owners, support teams, and automation engineers use this skill to import n8n workflows that automate eCommerce order confirmation, customer callbacks, return and FAQ routing, retry handling, outbound campaigns, status updates, CRM logging, and daily reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated workflow endpoints can trigger calls, messages, or order-record changes using the operator's credentials.

Mitigation: Deploy the workflows only behind authenticated, signed, and rate-limited webhooks, and validate order IDs, phone numbers, statuses, and state transitions server-side.

Risk: Request-controlled confirmation URLs and broad provider credentials can increase abuse or data-exposure impact.

Mitigation: Remove request-controlled confirmation URLs and use least-privilege credentials for voice, messaging, spreadsheet, store, CRM, and email providers.

Risk: Outbound calls, messages, transcripts, and customer records can create privacy, consent, retention, and telecom compliance obligations.

Mitigation: Document customer consent, privacy notices, transcript retention, spreadsheet access controls, and applicable telecom rules before enabling outbound communications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mhmalvi/skills/ecomm-ai-voice-agent)
- [Vapi API endpoint](https://api.vapi.ai)
- [Twilio API endpoint](https://api.twilio.com/2010-04-01)

## Skill Output:

**Output Type(s):** [markdown, configuration, code, shell commands, guidance]

**Output Format:** [Markdown guidance with n8n workflow JSON files and environment-variable configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires n8n credentials and environment variables for Vapi, Twilio, Google Sheets, store and CRM providers, messaging, and email.]

## Skill Version(s):

1.2.2 (source: server release metadata; artifact frontmatter and _meta.json report 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

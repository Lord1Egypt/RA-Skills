## Description: <br>
Automated cold email outreach pipeline using Resend API that builds prospect lists, enriches contact information, sends personalized cold emails with drip follow-ups, and tracks responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[merjua14](https://clawhub.ai/user/merjua14) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, growth, and operations teams use this skill to build prospect lists, personalize outbound email campaigns, send rate-limited Resend messages, manage drip follow-ups, and track campaign outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed for cold outreach and combines contact scraping or enrichment with live outbound email sending. <br>
Mitigation: Use dry-run first, review the recipient list and message copy, and run only campaigns where the sender controls the sending domain. <br>
Risk: Campaigns can process contact data and send unsolicited messages without sufficient safeguards. <br>
Mitigation: Confirm a lawful basis to process contact data, include unsubscribe and do-not-contact suppression controls, and honor removal requests before sending follow-ups. <br>
Risk: Additional enrichment or follow-up scripts may change the data handling or sending behavior. <br>
Mitigation: Review and separately approve enrichment and follow-up scripts before operational use. <br>


## Reference(s): <br>
- [Email Deliverability Guide](references/deliverability.md) <br>
- [Proven Cold Email Templates](references/templates.md) <br>
- [Resend Domains API](https://api.resend.com/domains) <br>
- [ClawHub Skill Page](https://clawhub.ai/merjua14/cold-email-outreach) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, template text, and JavaScript campaign code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses RESEND_API_KEY for live email sending; supports dry-run mode before delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

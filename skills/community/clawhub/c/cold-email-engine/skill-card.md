## Description: <br>
Automated cold email outreach system with lead enrichment, personalized templates, drip sequences, and CAN-SPAM compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[merjua14](https://clawhub.ai/user/merjua14) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and growth operators use this skill to prepare outbound email campaigns, enrich lead records, personalize messages, run drip follow-ups, and track sends while applying stated deliverability and compliance controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real cold-outreach email using provider credentials, and server security evidence says disclosure and safeguards are not clear enough for that external-facing authority. <br>
Mitigation: Install only when cold-email automation is intentional, use dry-run or sandbox recipients first, and manually approve campaigns before live sending. <br>
Risk: Lead enrichment and outreach can affect privacy, consent, suppression-list, anti-spam, and removal-request obligations. <br>
Mitigation: Confirm recipient lists manually, maintain suppression and unsubscribe handling, and verify each campaign complies with applicable consent, anti-spam, and privacy requirements. <br>
Risk: Email-provider API keys or SMTP credentials are required for live sending. <br>
Mitigation: Use scoped provider keys, store credentials outside committed files, and rotate keys if they are exposed. <br>


## Reference(s): <br>
- [Email Deliverability Guide](references/deliverability.md) <br>
- [Proven Cold Email Templates](references/templates.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/merjua14/cold-email-engine) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with command examples, configuration JSON, CSV logs, and generated email text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write send logs and enriched lead CSV files; can send live email through configured providers unless run in dry-run mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

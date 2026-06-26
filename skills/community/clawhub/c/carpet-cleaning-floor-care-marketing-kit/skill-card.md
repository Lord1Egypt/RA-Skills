## Description: <br>
Generates marketing copy, service pages, review/referral messaging, digital ads, and B2B outreach templates for carpet cleaning and floor care businesses with built-in claim guardrails for certifications, equipment specs, and advertising compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gitflopez](https://clawhub.ai/user/gitflopez) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams, agencies, and carpet cleaning or floor care operators use this skill to draft localized campaign assets, service-page copy, schema snippets, review requests, and outreach templates while preserving required business, certification, product, and consent checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated marketing claims can be inaccurate or noncompliant if license numbers, certifications, EPA registration numbers, testimonials, consent status, or local advertising rules are wrong or missing. <br>
Mitigation: Require human review before publication or outreach, and verify all business credentials, product registrations, testimonials, opt-out handling, and jurisdiction-specific advertising requirements against authoritative records. <br>
Risk: Outreach templates could be misused for unsolicited or automated email or SMS campaigns. <br>
Mitigation: Use the generated copy only with documented consent, working unsubscribe or STOP handling, and a human approval step before any messages are sent. <br>
Risk: The artifact contains guidance about regulated or technical carpet-care claims that may vary by service scope, product, location, and customer facts. <br>
Mitigation: Treat generated claims as drafts and confirm drying-time ranges, equipment specifications, fiber-care language, and health or allergen statements with qualified business staff before use. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/gitflopez/carpet-cleaning-floor-care-marketing-kit) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Marketing plan](artifact/MARKETING.md) <br>
- [Seasonal campaign and emergency hook prompt](artifact/prompts/01-lsa-gbp-hook.md) <br>
- [Service pages and schema prompt](artifact/prompts/02-service-pages-schema.md) <br>
- [Reputation and referral prompt](artifact/prompts/03-reputation-referral.md) <br>
- [Digital ads and B2B outreach prompt](artifact/prompts/04-b2b-outreach-system.md) <br>
- [Example output: Desert Fresh Carpet Care](artifact/example/desert_fresh_carpet_care_henderson.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown prompts and generated marketing assets, with JSON-LD code blocks where schema output is requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on user-supplied business details, certifications, equipment specifications, product registrations, review data, and commercial targets.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

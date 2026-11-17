## Description:

Runs a Node.js cold email workflow that imports CSV leads, fills personalized templates, sends through Resend or SendGrid with rate limits and suppression checks, logs sends, and provides basic lead-email enrichment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[merjua14](https://clawhub.ai/user/merjua14)

### License/Terms of Use:

MIT-0

## Use Case:

External sales or growth teams and developers can use this skill to assemble and run outbound email campaigns from lead CSVs. Review lawful basis, consent, suppression, and deliverability controls before live sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advertised compliance and automation claims may exceed implemented safeguards.

Mitigation: Verify lawful basis, unsubscribe handling, suppression behavior, drip follow-ups, bounce or reply tracking, and provider configuration before live sending.

Risk: Live sending and website enrichment can contact external services and process lead or contact data.

Mitigation: Prefer dry runs first, scope API keys, validate lead sources and enrichment domains, and treat generated CSVs and logs as untrusted data.

Risk: Suppression-list path handling and enrichment domain validation need tightening.

Mitigation: Constrain file paths to an approved working directory, sanitize domains before enrichment, and review code changes before deployment.

## Reference(s):

- [Email Deliverability Guide](artifact/references/deliverability.md)
- [Proven Cold Email Templates](artifact/references/templates.md)
- [Cold Email Engine on ClawHub](https://clawhub.ai/merjua14/skills/cold-email-engine)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command examples, Node.js scripts, JSON configuration, and CSV inputs or outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can perform live email sending when API keys are configured; use dry-run mode and review lead, suppression, and generated CSV data before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

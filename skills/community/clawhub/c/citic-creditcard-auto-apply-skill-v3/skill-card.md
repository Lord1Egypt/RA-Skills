## Description:

Recommends CITIC Bank credit cards from official CITIC credit-card pages and helps an agent prefill official application forms while stopping before final submission for applicant confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgmsmile](https://clawhub.ai/user/lgmsmile)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to compare CITIC Bank credit cards against a customer profile, generate top-card recommendations, extract user-authorized applicant fields from the workspace, and prepare a browser-assisted official form prefill workflow.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill handles highly sensitive applicant and financial data, and generated output files may store raw values in plaintext.

Mitigation: Use only in a private workspace, avoid committing or logging real ID numbers or financial details, and treat generated outputs as sensitive personal financial data.

Risk: Workspace memory or profile files could be scanned before the user has intentionally authorized use of those records.

Mitigation: Run the extractor or plan builder only after explicit user authorization, and present masked candidate fields with sources and confidence before any browser prefill.

Risk: Browser automation in a credit-card application flow could cross into consent, identity verification, or final submission steps.

Mitigation: Stop at CAPTCHA, SMS or OTP verification, face verification, signature, credit authorization, agreement consent, or final submit controls and require the applicant to complete those steps personally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lgmsmile/skills/citic-creditcard-auto-apply-skill-v3)
- [CITIC Bank Credit Card official site](https://creditcard.ecitic.com/)
- [Browser workflow notes](docs/browser_workflow.md)
- [Security notes](docs/security_notes.md)
- [Card catalog](data/card_catalog.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown recommendations, JSON recommendation and prefill-plan payloads, shell command examples, and browser-action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated candidate fields and prefill plans may contain sensitive personal financial data and should be reviewed by the applicant and kept private.]

## Skill Version(s):

1.0.0 (source: server release; artifact frontmatter states 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Automates client onboarding from inquiry to project kickoff, including intake processing, proposal and contract generation, Stripe payment collection, welcome emails, CRM updates, and project setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[merjua14](https://clawhub.ai/user/merjua14)

### License/Terms of Use:

MIT-0

## Use Case:

Small business operators, agencies, and client service teams use this skill to automate routine onboarding after a new inquiry, from data capture through contract, payment, welcome messaging, CRM logging, and project setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send contracts, payment links, CRM updates, or scheduled client emails without human review.

Mitigation: Add explicit human approval before external messages, contracts, payment links, or CRM changes are sent or applied.

Risk: The artifact's welcome sequence includes sending access credentials by email.

Mitigation: Use secure account invitations or one-time activation links instead of emailing passwords, API keys, or reusable credentials.

Risk: The workflow handles client intake, payment, and project information that may include sensitive business or personal data.

Mitigation: Define how client data is collected, stored, shared, retained, and deleted before deployment.

## Reference(s):

- [Client Onboarding Automator on ClawHub](https://clawhub.ai/merjua14/skills/client-onboarding-automator)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and structured configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May draft client emails, proposals, contracts, payment-link setup steps, CRM updates, project tasks, and onboarding reminders.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

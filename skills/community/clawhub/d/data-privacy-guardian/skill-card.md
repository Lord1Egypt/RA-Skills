## Description:

Provides personal data privacy and cybersecurity guidance for privacy checks, password practices, phishing and scam recognition, social media privacy settings, device security, app permissions, backups, digital footprint cleanup, and incident response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to receive structured privacy and cybersecurity advice, including privacy health reports, password hygiene recommendations, phishing and scam triage, platform privacy setting guidance, backup planning, and incident response steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The learning feature can retain user preferences, error notes, or sensitive security context locally without clear consent or limits.

Mitigation: Disable learning by default or make it explicit and opt-in, limit stored fields, and provide a clear way to inspect and delete stored data.

Risk: The skill describes automatic updates to its own skill instructions after repeated errors or usage, which can change behavior without review.

Mitigation: Require human review before any skill instruction changes and rescan the modified skill before deployment.

Risk: Privacy and incident-response advice may be incomplete for active account theft, financial loss, ransomware, or data exposure.

Mitigation: Frame outputs as guidance rather than a guarantee and direct users with active incidents to official support channels, law enforcement, or qualified security professionals.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with checklists, risk assessments, action plans, and optional bash command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include privacy risk scores, prioritized recommendations, emergency response steps, and locally stored learning preferences when the learning feature is used.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

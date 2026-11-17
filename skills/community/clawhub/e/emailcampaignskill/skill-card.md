## Description:

Agent-safe workflows for campaign briefs, audience logic, creative QA, launch readiness, and post-send analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polnikale](https://clawhub.ai/user/polnikale)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan, audit, QA, and improve email campaign workflows while separating recommendations from live-system actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email campaign guidance could affect live sends, contact imports, suppression rules, DNS/authentication settings, or production automations.

Mitigation: Require explicit human approval before sending email, importing contacts, changing suppressions, changing DNS/authentication, or editing production automations.

Risk: Campaign recommendations can be wrong if audience eligibility, consent, suppression state, deliverability context, or source evidence is missing.

Mitigation: Validate inclusions, exclusions, consent, suppression logic, expected counts, and supporting source material before acting on recommendations.

## Reference(s):

- [Email Campaign Skill Operating Checklist](references/operating-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces campaign briefs, audience QA tables, creative reviews, launch checklists, test plans, and post-send retrospectives with explicit approval gates for live or high-impact actions.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

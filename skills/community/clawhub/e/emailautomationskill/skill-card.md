## Description:

Helps agents plan, review, implement, audit, and improve email automation work focused on behavioral triggers, lifecycle journeys, governance, and operational safeguards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polnikale](https://clawhub.ai/user/polnikale)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, lifecycle marketers, and email operations teams use this skill to plan, audit, and improve behavioral and lifecycle email automations with clear QA checks, governance gates, and approval boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recommendations could affect live sends, contact imports, suppression rules, DNS or authentication settings, or production journeys if executed without review.

Mitigation: Require explicit approval and confirm the human owner, approval process, rollback plan, consent state, suppression state, and production impact before any real provider change.

Risk: Missing, stale, or delayed automation data could produce duplicate, late, irrelevant, or non-compliant messages.

Mitigation: Verify event schema, data freshness, suppression rules, consent state, frequency caps, test contacts, and rollback steps before recommending automation changes.

## Reference(s):

- [Email Automation Skill Operating Checklist](references/operating-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/polnikale/skills/emailautomationskill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown guidance with automation contracts, trigger inventories, QA plans, overlap audits, governance checklists, and journey optimization recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates recommendations from live-system actions and requires explicit approval before provider changes, sends, imports, suppression edits, DNS changes, or production automation edits.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

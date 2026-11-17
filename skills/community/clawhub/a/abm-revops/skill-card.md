## Description:

RevOps helps agents design and optimize revenue operations systems for lead lifecycle management, scoring, routing, CRM automation, pipeline hygiene, and marketing-to-sales handoffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariokarras](https://clawhub.ai/user/mariokarras)

### License/Terms of Use:

MIT-0

## Use Case:

External RevOps practitioners, GTM teams, and operators use this skill to turn business context into lifecycle definitions, lead scoring models, routing rules, CRM automation plans, pipeline hygiene processes, and metrics dashboard specifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CRM, Slack/email, enrichment, and advertising automations can expose lead or contact data beyond the intended audience.

Mitigation: Review automations with the relevant system owner, limit notifications to need-to-know recipients, and prefer CRM links over full behavioral histories in chat or email.

Risk: Syncing contacts to enrichment tools or advertising platforms can conflict with consent, opt-out, or jurisdictional requirements.

Mitigation: Verify consent, opt-outs, and applicable regional rules before syncing contacts or audiences to external systems.

Risk: Workflow recipes can create incorrect lead assignments, SLA escalations, or lifecycle changes if copied into production without local validation.

Mitigation: Test CRM workflow rules with sample records and have the CRM or RevOps owner approve routing, stage, and escalation behavior before rollout.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mariokarras/skills/abm-revops)
- [Automation Playbooks](artifact/references/automation-playbooks.md)
- [Lifecycle Stage Definitions](artifact/references/lifecycle-definitions.md)
- [Lead Routing Rules](artifact/references/routing-rules.md)
- [Lead Scoring Models](artifact/references/scoring-models.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown documents with tables, checklists, scoring specifications, routing rules, automation recipes, and dashboard specifications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform-specific CRM guidance when the user's CRM is known.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter metadata.version is 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

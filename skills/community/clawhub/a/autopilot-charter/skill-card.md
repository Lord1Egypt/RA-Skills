## Description:

Decide which recurring rituals to put on autopilot, which to keep manual, how to set up recurring AI runs, which reports or briefings could run on a schedule, and how to design an automation charter for a team.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and team leads use this skill to decide which recurring reports, briefings, reviews, monitors, or digests should be automated, drafted with assistance, or kept manual. It produces a charter with rationale, guardrails, and rollout order for scheduling lower-risk rituals first.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Later automation setup may grant agents access to sensitive systems such as inboxes, CRMs, analytics, or publishing workflows.

Mitigation: Review access scopes, source reachability, and approval gates before wiring any ritual to a scheduled runner.

Risk: Automated or assisted recurring outputs may be wrong, stale, missing, or misleading for their audience.

Mitigation: Require review gates for audience-facing outputs, include staleness markers, define failure behavior, and set kill criteria for each automated ritual.

Risk: Teams may over-automate judgment-bearing rituals or high-blast-radius reports.

Mitigation: Classify each ritual as Automate, Assist, or Keep Manual using input reachability, structural stability, cost of error, and delta-shaped value; start rollout with low-risk rituals.

## Reference(s):

- [Autopilot Charter skill page](https://clawhub.ai/mohitagw15856/skills/autopilot-charter)
- [Autopilot Charter homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/autopilot-charter.html)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, Configuration instructions]

**Output Format:** [Markdown with tables, checklist-style quality checks, and concise recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a ritual inventory, automate/assist/manual classifications, guardrails for automated rituals, rollout order, and next steps.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Runs NPI phase-gate reviews for EVT, DVT, and PVT by scoring exit criteria, triaging open issues, analyzing yield, tracking waivers, and producing a go, conditional-go, or no-go recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Hardware NPI, manufacturing, quality, and product teams use this skill to evaluate whether an EVT, DVT, or PVT build is ready to exit its current phase or enter the next one. It turns build results, open issues, exit criteria, and schedule pressure into a structured gate review with explicit conditions and waivers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gate reviews can include confidential product, defect, schedule, cost, and manufacturing data.

Mitigation: Use appropriate access controls and avoid providing information beyond what is needed for the review.

Risk: Incomplete or weak build evidence can lead to an overconfident phase-gate recommendation.

Mitigation: Require denominators, station-by-station yield data, explicit pass/fail/no-data scoring, and human review of any go or conditional-go decision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohitagw15856/skills/evt-dvt-pvt-gate-review)
- [Skill homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/evt-dvt-pvt-gate-review.html)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown gate review document with scorecards, triage tables, yield analysis, waiver register, and recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided build, yield, issue, criteria, and schedule data; marks missing criteria as no data instead of assuming a pass.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

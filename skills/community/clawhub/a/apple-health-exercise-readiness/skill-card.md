## Description:

Analyzes a user-provided Apple Health export to estimate today's exercise readiness, recommend one of four activity levels, and explain the key health signals behind the recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lynnshaw](https://clawhub.ai/user/lynnshaw)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn Apple Health export data into a clear daily exercise recommendation with supporting context from sleep, HRV, resting heart rate, blood oxygen, respiratory rate, and recent activity. The skill is intended for health-management guidance and does not provide medical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apple Health exports contain sensitive health data that may be visible to the agent session during analysis.

Mitigation: Use only exports you created yourself and run the skill only when you are comfortable sharing export-derived metrics with the active agent session.

Risk: Saved JSON reports can persist health-derived metrics in the selected output directory.

Mitigation: Use --out only with a directory intended for storing a health-data report and manage that output according to your privacy requirements.

Risk: Exercise readiness recommendations are health-management guidance, not medical diagnosis.

Mitigation: Treat abnormal blood oxygen, resting heart rate, or other warning signals as reasons to rest and consult a clinician when symptoms or abnormal readings persist.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lynnshaw/skills/apple-health-exercise-readiness)
- [Publisher profile](https://clawhub.ai/user/lynnshaw)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown-style exercise readiness report, with optional JSON output from the bundled Python analyzer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a score, four-level activity recommendation, supporting signals, warning signals, and optional exercise_readiness.json file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

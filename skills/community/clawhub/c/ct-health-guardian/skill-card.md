## Description:

Proactive health monitoring for AI agents. Apple Health integration, pattern detection, anomaly alerts. Built for agents caring for humans with chronic conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ctsolutionsdev](https://clawhub.ai/user/ctsolutionsdev)

### License/Terms of Use:

MIT

## Use Case:

External users and agent builders use Health Guardian to import Apple Health export data, analyze local health patterns, and surface anomaly alerts for people with chronic conditions or disability-related care needs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive health data and ongoing health alerts.

Mitigation: Use it only with explicit consent from the person whose health data is processed, and keep health data and alert handling local unless the user intentionally accepts third-party messaging risk.

Risk: Health alerts and summaries may be mistaken for medical advice or emergency detection.

Mitigation: Present outputs as informational signals only, require human review for health decisions, and do not rely on the skill for emergency detection or medical diagnosis.

Risk: Incorrect data paths or missing and inconsistent scripts may prevent reliable operation.

Mitigation: Review and correct configured paths and scripts before relying on imports, summaries, or alerts.

## Reference(s):

- [Health Auto Export](https://apps.apple.com/app/health-auto-export/id1115567069)
- [ClawHub skill page](https://clawhub.ai/ctsolutionsdev/skills/ct-health-guardian)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with JSON configuration examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local import results, health summaries, and alert text; outputs should not be treated as medical advice or emergency detection.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

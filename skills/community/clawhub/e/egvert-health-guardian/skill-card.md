## Description:

Proactive health monitoring for AI agents with Apple Health integration, pattern detection, and anomaly alerts for agents caring for humans with chronic conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ctsolutionsdev](https://clawhub.ai/user/ctsolutionsdev)

### License/Terms of Use:

MIT

## Use Case:

External users and agent developers use this skill to import Apple Health exports, monitor health patterns, and surface configurable anomaly alerts for caregiver-style workflows. Alerts should be treated as informational rather than medical advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive health-derived data.

Mitigation: Use it only with informed consent, restrict which Apple Health files it can read, and protect the local data directory.

Risk: Health alerts may be mistaken for medical advice.

Mitigation: Treat alerts as informational and require appropriate human or clinical review before acting on them.

Risk: Third-party alert channels can expose health-derived information.

Mitigation: Disable external alerts or use only approved channels that the monitored person accepts.

Risk: Persistent monitoring can run beyond the user's intended scope.

Mitigation: Review cron or heartbeat automation before enabling it and document who receives alerts.

## Reference(s):

- [Health Guardian ClawHub release](https://clawhub.ai/ctsolutionsdev/skills/egvert-health-guardian)
- [Health Auto Export](https://apps.apple.com/app/health-auto-export/id1115567069)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with JSON configuration and local JSON data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local health readings, summaries, and alert text from Apple Health export files.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

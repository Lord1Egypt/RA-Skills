## Description:

Generate comprehensive daily health reports from Garmin Connect data with professional running analysis (Heart Rate Zones, TRIMP, Jack Daniels VDOT).

This skill is ready for commercial/non-commercial use.

## Publisher:

[gzzzj](https://clawhub.ai/user/gzzzj)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to authenticate with Garmin Connect, retrieve personal health and activity data, and generate daily reports with sleep, heart-rate, steps, running-load, VDOT, recovery, and seven-day trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Garmin authentication tokens and local health history can expose sensitive account and health data if the host or data directories are shared or compromised.

Mitigation: Install only on a trusted machine, treat token and history files as sensitive, and protect ~/.garmin-health-report and ~/.garmin_health_report with owner-only permissions.

Risk: Logout may not remove all garth OAuth token files used by the skill.

Mitigation: Before relying on logout, verify and remove oauth1_token.json and oauth2_token.json under ~/.garmin-health-report.

Risk: The garth dependency is declared as a lower-bound version instead of a reviewed pinned release.

Mitigation: Pin garth to a reviewed version before deployment and review dependency updates before installing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gzzzj/skills/garmin-health-report)
- [Project Homepage](https://github.com/yourusername/garmin-health-report)
- [garth Garmin Connect library](https://github.com/matin/garth)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Formatted plain text report with command-line setup and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include personal health metrics, running analysis, recommendations, and seven-day trend summaries when Garmin data is available.]

## Skill Version(s):

2.0.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

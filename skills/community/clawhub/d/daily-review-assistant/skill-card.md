## Description:

Generate A-share daily review report (stock-analysis/daily_review.py). Supports --email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnxufei-tech](https://clawhub.ai/user/cnxufei-tech)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate daily A-share market review reports in Markdown, including market overview, leaderboards, sentiment signals, and next-day strategy. It can optionally send the generated report by SMTP email when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill executes a workspace Python script that is not bundled in the artifact.

Mitigation: Review stock-analysis/daily_review.py in the target workspace before running the skill.

Risk: Optional email delivery can send reports to configured recipients through SMTP.

Mitigation: Inspect email_config.json recipient settings before using --email and use an SMTP app password or authorization code rather than an account password.

Risk: Market data collection depends on AkShare data sources that may intermittently disconnect.

Mitigation: Expect occasional data-source failures and verify report contents before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cnxufei-tech/skills/daily-review-assistant)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Files]

**Output Format:** [Markdown report saved under stock-analysis/reports/YYYYMMDD.md, with optional SMTP email delivery.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, AkShare, and the workspace stock-analysis/daily_review.py script; email sending depends on local email configuration and SMTP_PASSWORD.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

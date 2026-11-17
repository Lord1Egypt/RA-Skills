## Description:

Analyze application logs to produce actionable error digests with pattern detection, severity classification, trend analysis, and remediation recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site reliability engineers, and operations teams use this skill to inspect application or server logs, group recurring failures, classify severity, identify trends, and get remediation guidance during incidents or health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analyzed logs and generated reports may contain sensitive operational or personal data.

Mitigation: Run the skill only on selected log files or directories and limit access to generated reports.

Risk: Untrusted log content may be included in generated Markdown reports.

Mitigation: Prefer JSON or text output for untrusted logs, or review Markdown output before sharing or rendering it.

Risk: CI or scheduled usage can affect operational workflows through nonzero exit codes.

Mitigation: Review filters, severity thresholds, and exit-code handling before wiring the skill into CI, cron, or alerting workflows.

## Reference(s):

- [Error Pattern Reference](references/error-patterns.md)
- [ClawHub release page](https://clawhub.ai/charlie-morrison/skills/cm-log-analyzer)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Text, JSON, or Markdown log analysis reports with remediation recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use exit codes 0, 1, or 2 to reflect clean, error, or fatal findings in automation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

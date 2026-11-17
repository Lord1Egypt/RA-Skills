## Description:

Analyze origin web access logs for CC attacks, proxy-pool bots, scanning probes, login brute force, abnormal crawlers, traffic surges, status-code surges, and slow resource consumption, then produce an actionable security report with mitigation advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and site operators use this skill to analyze user-provided Nginx, Apache, or IIS access logs for web-application attack patterns and operational impact. The skill produces evidence-backed reports that support incident triage and mitigation planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access logs may contain IP addresses, URLs, user agents, and other operational data.

Mitigation: Only provide logs that are approved for local analysis, and redact or minimize sensitive fields before use when policy requires it.

Risk: The skill writes a generated report to disk and may fall back to the current working directory if its default output directory is not writable.

Mitigation: Use an explicit output path when report location or retention needs to be controlled.

## Reference(s):

- [Log Parsing Module](artifact/references/log_parsing.md)
- [Attack Detection Module](artifact/references/attack-detection.md)
- [Report Generation Module](artifact/references/report-generation.md)
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-web-application-attacks-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Plain text or Markdown report with a Structured Findings JSON section]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are generated locally from a user-provided access log and include an Executive Summary, detailed attack evidence, mitigation recommendations, and machine-readable findings.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

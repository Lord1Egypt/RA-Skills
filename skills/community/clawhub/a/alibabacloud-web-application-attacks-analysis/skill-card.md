## Description:

Analyze Nginx, Apache, and IIS access logs to identify common web attack patterns and produce a security report with actionable mitigation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security staff, and site operators use the skill to review user-provided Nginx, Apache, or IIS access logs, identify likely attack patterns, and prioritize mitigation actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A report-writing flaw may overwrite the access log being analyzed.

Mitigation: Protect original logs, verify the report destination, and avoid installation until the overwrite issue is addressed and the script is reviewed.

Risk: An issue in traffic attribution may identify the wrong source as abusive.

Mitigation: Verify suspicious source addresses against trusted proxy and origin records before taking blocking action.

## Reference(s):

- [Log parsing reference](artifact/references/log_parsing.md)
- [Attack detection reference](artifact/references/attack-detection.md)
- [Report generation reference](artifact/references/report-generation.md)
- [ClawHub release page](https://clawhub.ai/sdk-team/skills/alibabacloud-web-application-attacks-analysis)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON, Mitigation guidance]

**Output Format:** [Text or Markdown report with a structured JSON findings section]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [English ASCII output; analyzes a user-provided access log.]

## Skill Version(s):

0.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

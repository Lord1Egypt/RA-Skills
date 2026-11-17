## Description:

AI runtime security monitoring — context graph analysis, runtime audit log correlation with CVE findings, and vulnerability analytics queries. Use when the user mentions runtime monitoring, context graphs, lateral movement analysis, audit log correlation, or vulnerability analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msaad00](https://clawhub.ai/user/msaad00)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and security engineers use this skill to analyze AI agent runtime context, correlate user-provided audit logs with CVE findings, and query vulnerability trends and runtime events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security analysis was partial because the referenced `proxy-audit.jsonl` runtime file was not included.

Mitigation: Review the audit log or confirm it is not needed before installing; the benign scanner verdict is not a guarantee of safety.

Risk: Optional ClickHouse analytics can persist runtime audit data, and the audit data may include credential environment variable names.

Mitigation: Configure ClickHouse only when needed, use an operator-controlled endpoint, and do not include raw credential values in audit data.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/msaad00/skills/agent-bom-runtime)
- [Project homepage](https://github.com/koda-ai-studio/agent-bom)
- [PyPI package](https://pypi.org/project/agent-bom/)
- [OpenSSF Scorecard](https://securityscorecards.dev/viewer/?uri=github.com/koda-ai-studio/agent-bom)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text]

**Output Format:** [Text and structured analytics results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the scan results, user-provided audit log, and analytics query.]

## Skill Version(s):

0.115.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

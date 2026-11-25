## Description:

AI runtime security monitoring — context graph analysis, runtime audit log correlation with CVE findings, and vulnerability analytics queries. Use when the user mentions runtime monitoring, context graphs, lateral movement analysis, audit log correlation, or vulnerability analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msaad00](https://clawhub.ai/user/msaad00)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and security engineers use this skill to analyze agent context graphs, correlate runtime audit logs with vulnerability findings, and query security analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The referenced proxy-audit.jsonl file was unavailable for scanner review.

Mitigation: Before use, confirm whether you expect the skill to use this file and review the user-provided audit log.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/msaad00/skills/agent-bom-runtime)
- [Project homepage](https://github.com/koda-ai-studio/agent-bom)
- [PyPI package](https://pypi.org/project/agent-bom/)
- [OpenSSF Scorecard](https://securityscorecards.dev/viewer/?uri=github.com/koda-ai-studio/agent-bom)

## Skill Output:

**Output Type(s):** [Analysis, Text]

**Output Format:** [Text and structured analysis results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analysis is based on supplied scan results and user-provided audit logs; optional ClickHouse analytics is operator-configured.]

## Skill Version(s):

0.115.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

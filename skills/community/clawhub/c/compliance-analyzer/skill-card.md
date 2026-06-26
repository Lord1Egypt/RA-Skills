## Description: <br>
Maps AWS environments against CIS, SOC 2, HIPAA, or PCI-DSS controls with prioritized remediation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolnagpal](https://clawhub.ai/user/anmolnagpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Cloud security, compliance, and platform teams use this skill to analyze exported AWS Config and Security Hub data, map findings to common compliance frameworks, and prepare prioritized remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AWS exports or pasted findings may include secrets or unrelated sensitive account details. <br>
Mitigation: Remove secrets and unnecessary sensitive fields before sharing data with the agent, and use least-privilege read-only AWS access when creating exports. <br>
Risk: Generated remediation commands may change AWS account configuration if run without review. <br>
Mitigation: Review generated remediation commands and runbooks before applying them in an AWS account. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with tables and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces compliance scores, control status tables, gap priority matrices, remediation runbooks, evidence narratives, and AWS Config rule suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Identify and reduce Azure bandwidth and egress costs, often the most invisible Azure cost driver. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolnagpal](https://clawhub.ai/user/anmolnagpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, cloud engineers, and FinOps teams use this skill to analyze exported Azure bandwidth cost data and network topology, then identify egress reduction opportunities with ROI estimates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Azure exports or pasted CLI output may contain secrets or unnecessary account details. <br>
Mitigation: Review and redact inputs before sharing, and provide only the billing and network fields needed for the analysis. <br>
Risk: Suggested commands or infrastructure snippets could be applied in the wrong Azure tenant or subscription. <br>
Mitigation: Run any Azure CLI commands only in the intended tenant and subscription with read-only access, and review generated Bicep or ARM snippets before use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown analysis with cost breakdowns, heatmaps, ROI tables, recommendations, and Bicep or ARM snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; uses user-provided exports or read-only CLI output and does not connect to Azure directly.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

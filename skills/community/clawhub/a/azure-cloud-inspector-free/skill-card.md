## Description: <br>
Azure Cloud Inspector Free helps agents run Azure CLI inspections for resource inventory, health checks, exposure discovery, configuration drift review, risk scoring, and Markdown reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud operators and developers use this skill to guide read-oriented Azure CLI inspection workflows, identify exposed resources and configuration drift, score operational risk, and produce Markdown inspection reports for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to run Azure CLI commands in the user's active Azure login context. <br>
Mitigation: Use a Reader-scoped account where possible and review commands before execution. <br>
Risk: The security review notes a mismatch between read-only positioning and artifact text that mentions modify or delete capability. <br>
Mitigation: Require explicit confirmation before any write, delete, scale, or credential-related command. <br>
Risk: Generated snapshots and reports may persist Azure inventory details under /tmp. <br>
Mitigation: Inspect, protect, or remove generated /tmp snapshot and report files after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/azure-cloud-inspector-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Azure CLI and bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local /tmp Azure inventory snapshots and Markdown inspection reports when the user runs the suggested commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version and artifact metadata.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Analyze Azure Activity Logs and Sentinel incidents for suspicious patterns and attack indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolnagpal](https://clawhub.ai/user/anmolnagpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Security analysts, cloud administrators, and incident responders use this skill to review exported Azure Activity Logs and Microsoft Sentinel incidents, identify suspicious operations, build an incident timeline, and draft containment and detection guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Log exports can contain sensitive tenant, identity, IP address, or incident details. <br>
Mitigation: Provide only the narrow exports needed for the incident and redact secrets or unrelated tenant data before sharing. <br>
Risk: Suggested Azure CLI containment commands may affect access or resources if run without review. <br>
Mitigation: Manually review and adapt any proposed Azure CLI commands before executing them in an Azure environment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, KQL queries, guidance] <br>
**Output Format:** [Markdown with tables and inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces threat summaries, incident timelines, findings tables, attack narratives, containment actions, and Sentinel KQL detection queries from user-provided exports.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Coordinates incident response, communications, resolution tracking, post-mortems, metrics, and runbook creation using SRE and enterprise incident response practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtsatryan](https://clawhub.ai/user/mtsatryan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, SREs, and incident responders use this skill to structure incident declaration, coordination, stakeholder communication, root cause analysis, post-mortems, metrics, and runbook drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incident prompts and generated reports can contain confidential customer, outage, or business-impact details. <br>
Mitigation: Avoid pasting sensitive incident details unless approved for the agent environment; redact customer, credential, and business-impact data before use. <br>
Risk: Generated severity, ETA, impact, or stakeholder communication may be incomplete or misleading during a live incident. <br>
Mitigation: Have the incident commander or responsible lead verify severity, impact, status, ETA, and external communications before sending or acting on them. <br>
Risk: Runbook templates include shell command placeholders that may be unsuitable for a specific production system. <br>
Mitigation: Replace placeholders with approved, tested commands and review any command before execution. <br>


## Reference(s): <br>
- [Incident Manager examples](references/examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/mtsatryan/ah-incident-manager) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown templates, checklists, reports, and inline shell command placeholders] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces incident response artifacts for human review; no executable code is bundled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

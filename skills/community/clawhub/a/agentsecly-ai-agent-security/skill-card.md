## Description: <br>
Generate AI agent security advisories with threat analysis, MITRE ATT&CK mapping, severity scoring, and remediation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and AI governance teams use this skill to assess AI agent threats such as prompt injection, data leakage, model manipulation, and unauthorized access. It produces advisory-style guidance with MITRE ATT&CK mapping and remediation actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Assessment details provided by the user are sent to ToolWeb for analysis. <br>
Mitigation: Avoid including secrets, customer data, exact internal architecture, or sensitive incident details unless the organization has approved that use and reviewed ToolWeb's data-handling terms. <br>
Risk: The skill depends on a configured ToolWeb API key and may count successful API calls against the user's ToolWeb plan. <br>
Mitigation: Confirm API key access, quota, and billing expectations before using the skill in routine workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/agentsecly-ai-agent-security) <br>
- [ToolWeb API portal](https://portal.toolweb.in) <br>
- [ToolWeb platform](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown security advisory with severity score, MITRE ATT&CK mapping, threat analysis, and remediation actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; API results are presented to the user as an advisory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

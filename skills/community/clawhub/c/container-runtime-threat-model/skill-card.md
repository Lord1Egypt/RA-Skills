## Description: <br>
Generate container runtime threat models analyzing attack surfaces across container components, images, privileges, network exposure, and security controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform engineers, and security teams use this skill to generate STRIDE-based threat models for containerized applications and assess runtime risks across images, privileges, network exposure, security controls, and sensitive data handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends container architecture and security-control details to ToolWeb for analysis. <br>
Mitigation: Submit only information that is appropriate to share with ToolWeb, avoid secrets or unnecessary production identifiers, and review ToolWeb privacy, retention, and billing terms before use on sensitive systems. <br>
Risk: Threat-model results depend on the ToolWeb API response and the accuracy of the user-provided container details. <br>
Mitigation: Review generated findings before acting on them and validate high-impact mitigations against the deployed environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/container-runtime-threat-model) <br>
- [ToolWeb API portal](https://portal.toolweb.in) <br>
- [ToolWeb platform](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown threat model with STRIDE analysis, risk scores, attack trees, prioritized mitigations, and curl-based API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; sends container architecture and security-control details to the ToolWeb API.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

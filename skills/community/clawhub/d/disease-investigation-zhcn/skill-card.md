## Description: <br>
Guides disease research by combining literature, epidemiology, clinical guidelines, drug intelligence, patent context, clinical trials, and commercial-development evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patsnaplifescience](https://clawhub.ai/user/patsnaplifescience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Life-science researchers, pharmaceutical R&D teams, and commercial-development analysts use this skill to investigate disease mechanisms, epidemiology, standards of care, pipelines, patents, and market context with PatSnap life-science data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a PatSnap API key and connects to PatSnap's life-science MCP service. <br>
Mitigation: Install it only when you intend to use that service, store the API key in local agent configuration, and monitor API usage. <br>
Risk: Disease research questions may involve confidential patient, research, or business data sent through the configured service. <br>
Mitigation: Avoid submitting confidential data unless the PatSnap account terms and organization policies permit that use. <br>


## Reference(s): <br>
- [Disease Investigation Zhcn on ClawHub](https://clawhub.ai/patsnaplifescience/disease-investigation-zhcn) <br>
- [PatSnap Open Platform](https://open.patsnap.com) <br>
- [PatSnap Pharma Intelligence MCP Server](https://open.patsnap.com/marketplace/mcp-servers/096456) <br>
- [PatSnap Life Science](https://eureka.patsnap.com/ls-landing) <br>
- [PatSnap Developer Documentation](https://open.patsnap.com/devportal) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown reports with structured sections, citations or identifiers where applicable, and setup commands for MCP configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected PatSnap life-science MCP service before answering disease research queries.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

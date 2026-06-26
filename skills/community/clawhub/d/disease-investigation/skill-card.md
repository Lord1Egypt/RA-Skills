## Description: <br>
Conducts comprehensive disease investigations combining academic literature, epidemiological data, clinical guidelines, pharmaceutical intelligence, and clinical trial reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patsnaplifescience](https://clawhub.ai/user/patsnaplifescience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Life science and pharmaceutical R&D or business development users use this skill to investigate disease mechanisms, epidemiology, standards of care, pipelines, patent landscapes, and commercial viability for a disease or indication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive PatSnap API credentials for MCP access. <br>
Mitigation: Configure credentials only in trusted environments, verify MCP connectivity before use, and avoid exposing API keys in prompts, logs, or shared transcripts. <br>
Risk: The security scan verdict is suspicious because a helper workflow may run with broad local access and disabled approvals. <br>
Mitigation: Install only in trusted repositories, prefer approval-requiring execution settings where supported, and review generated or retrieved outputs before relying on them. <br>


## Reference(s): <br>
- [PatSnap Pharma Intelligence MCP Server](https://open.patsnap.com/marketplace/mcp-servers/096456) <br>
- [PatSnap Life Science](https://eureka.patsnap.com/ls-landing) <br>
- [PatSnap Dev Portal](https://open.patsnap.com/devportal) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown report with numbered sections, evidence references, and a conclusion] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PatSnap LifeScience MCP services and an API key for data retrieval.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

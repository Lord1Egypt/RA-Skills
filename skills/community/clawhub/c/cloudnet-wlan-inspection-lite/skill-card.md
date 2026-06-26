## Description: <br>
Cloudnet AI Inspection guides agents through a Cloudnet WLAN health inspection using mcporter and Cloudnet MCP data, then produces Chinese Markdown and DOCX inspection reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloudnet-skills](https://clawhub.ai/user/cloudnet-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network operations teams and developers use this skill to run quick daily WLAN inspections for named Cloudnet-managed sites, collect AC/AP/access-success data, and generate Chinese operational inspection reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires and may persist a Cloudnet API credential in config.json and mcporter configuration. <br>
Mitigation: Install only when Cloudnet WLAN inspection access is intended; treat config.json and mcporter configuration as secrets, avoid committing or sharing them, prefer a safer credential mechanism if available, and remove or rotate the bearer token when access is no longer needed. <br>
Risk: Inspection results and reports depend on external Cloudnet API data and agent extraction of the returned JSON. <br>
Mitigation: Review the source inspection data and generated report before using findings for operational remediation. <br>


## Reference(s): <br>
- [Cloudnet AI Inspection release page](https://clawhub.ai/cloudnet-skills/cloudnet-wlan-inspection-lite) <br>
- [Cloudnet MCP server endpoint](https://oasis.h3c.com/mcp-server/api/sse) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese Markdown and DOCX reports, command guidance, JSON intermediate data, and inspection summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Cloudnet API key, mcporter CLI configuration, and python-docx for DOCX output.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

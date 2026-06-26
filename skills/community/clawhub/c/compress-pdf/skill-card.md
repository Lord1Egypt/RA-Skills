## Description: <br>
Compress a user-provided PDF by uploading it to Cross-Service-Solutions, polling until completion, then returning a download URL for the compressed file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CrossServiceSolutions](https://clawhub.ai/user/CrossServiceSolutions) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to compress a selected PDF through the Cross-Service-Solutions API and receive a compressed-file download URL with job status and settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected PDFs are uploaded to an external Cross-Service-Solutions compression service and the compressed output is returned as a third-party-hosted download URL. <br>
Mitigation: Use this skill only with documents approved for that provider; avoid sensitive, regulated, or confidential PDFs unless the provider is approved for that data. <br>
Risk: The skill requires a Cross-Service-Solutions API key for Bearer-token authentication. <br>
Mitigation: Use a dedicated API key where possible, provide it through a secure secret or environment variable, and keep it out of logs and shared chat text. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/CrossServiceSolutions/compress-pdf) <br>
- [CrossServiceSolutions Publisher Profile](https://clawhub.ai/user/CrossServiceSolutions) <br>
- [Cross-Service-Solutions API Key Registration](https://login.cross-service-solutions.com/register) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON result plus Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns job status, compressed file download URL, file name, and compression settings when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

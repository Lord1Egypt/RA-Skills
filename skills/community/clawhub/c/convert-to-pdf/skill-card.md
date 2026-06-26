## Description: <br>
Convert one or multiple documents to PDF by uploading them to Cross-Service-Solutions, polling until completion, then returning download URL(s) for the converted PDF(s) (or a ZIP if multiple). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CrossServiceSolutions](https://clawhub.ai/user/CrossServiceSolutions) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to convert one or more user-selected documents into PDFs through the Cross-Service-Solutions API and return download URLs for the converted files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents are uploaded to an external PDF conversion service. <br>
Mitigation: Use non-sensitive test files first and avoid confidential or regulated documents unless the provider's privacy and retention terms meet the deployment requirements. <br>
Risk: The skill requires a Cross-Service-Solutions API key. <br>
Mitigation: Protect the API key, never echo or log it, and prefer a scoped or disposable key where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CrossServiceSolutions/convert-to-pdf) <br>
- [Cross-Service-Solutions API registration](https://login.cross-service-solutions.com/register) <br>
- [Solutions API convert endpoint](https://api.xss-cross-service-solutions.com/solutions/solutions/api/31) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files] <br>
**Output Format:** [JSON object with job status, output file metadata, and download URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return one PDF URL, multiple PDF URLs, or a ZIP URL depending on input count and service response.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

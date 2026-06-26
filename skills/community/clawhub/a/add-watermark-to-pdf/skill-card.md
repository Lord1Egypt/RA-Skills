## Description: <br>
Add a text watermark to one or multiple PDFs by uploading them to the Solutions API, polling until completion, then returning download URL(s) for the watermarked PDF(s) or a ZIP if multiple. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CrossServiceSolutions](https://clawhub.ai/user/CrossServiceSolutions) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to add visible text watermarks to one or more PDF files through the Cross-Service-Solutions API and retrieve downloadable outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected PDFs, filenames, watermark text, and API-authenticated requests are sent to a third-party API. <br>
Mitigation: Use only with documents approved for Cross-Service-Solutions processing; avoid confidential or regulated PDFs unless that service is approved for the user's use. <br>
Risk: The skill requires a bearer API key and permits an override of the API base URL. <br>
Mitigation: Keep the API key secret and revocable, and only override the base URL when the destination is intentionally trusted. <br>
Risk: The artifact script can include watermark text in the JSON result. <br>
Mitigation: Do not return watermark text downstream when the user considers it sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CrossServiceSolutions/add-watermark-to-pdf) <br>
- [Cross-Service-Solutions API registration](https://login.cross-service-solutions.com/register) <br>
- [Solutions API base URL](https://api.xss-cross-service-solutions.com/solutions/solutions) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, guidance] <br>
**Output Format:** [JSON with job status, output file metadata, and download URL fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes job ID, status, output file names, download URL(s), input filenames, and watermark text only when safe to return.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

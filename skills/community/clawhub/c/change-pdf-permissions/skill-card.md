## Description: <br>
Change a PDF's permission flags by uploading it to the Solutions API, polling until completion, then returning a download URL for the updated PDF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CrossServiceSolutions](https://clawhub.ai/user/CrossServiceSolutions) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to set PDF permission flags such as printing, editing, copying, form filling, annotations, and accessibility extraction, then receive a download URL for the updated PDF. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads PDFs and permission settings to a third-party API for processing. <br>
Mitigation: Use it only for documents that are approved for processing by api.xss-cross-service-solutions.com; avoid confidential, regulated, or customer documents unless that service is approved for the data. <br>
Risk: PDF permission flags may be enforced differently by different PDF viewers. <br>
Mitigation: Test the updated PDF in the viewer environments that matter before relying on the permissions for document control. <br>
Risk: The skill requires a Solutions API key. <br>
Mitigation: Provide the key through a secret or environment variable, and do not echo, log, or store it in prompts, files, or command history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CrossServiceSolutions/change-pdf-permissions) <br>
- [Solutions API registration](https://login.cross-service-solutions.com/register) <br>
- [Solutions API endpoint](https://api.xss-cross-service-solutions.com/solutions/solutions) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Structured JSON result with job status, download URL, file name, and final permission settings; guidance may include CLI command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a PDF file, permission flags, and a Solutions API key; returns an external download URL when the API job completes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

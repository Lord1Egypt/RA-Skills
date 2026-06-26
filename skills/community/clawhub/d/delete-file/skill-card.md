## Description: <br>
Delete a file from cloud storage by URL. Only the API key that uploaded the file can delete it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rishabhdugar](https://clawhub.ai/user/rishabhdugar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to delete PDF API Hub files they previously uploaded, especially for privacy compliance, storage cleanup, workflow cleanup, and sensitive document handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs a destructive delete operation against a cloud file URL. <br>
Mitigation: Confirm the exact uploaded-file URL before execution and avoid automatic use from ambiguous cleanup requests. <br>
Risk: The skill requires a sensitive PDF API Hub API key. <br>
Mitigation: Treat the API key as sensitive and install the skill only if you trust pdfapihub.com and need agents to delete files from that service. <br>


## Reference(s): <br>
- [PDF API Hub](https://pdfapihub.com) <br>
- [PDF API Hub Documentation](https://pdfapihub.com/docs) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with curl command examples and JSON request details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a PDF API Hub API key in the CLIENT-API-KEY header and a file URL previously returned by the upload endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

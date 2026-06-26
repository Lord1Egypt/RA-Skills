## Description: <br>
Queries task status from the AICNIC job management system by calling the job information API and extracting returned task fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bylikai](https://clawhub.ai/user/bylikai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, or users with an AICNIC job ID use this skill to retrieve task status and basic job metadata from the AICNIC job management system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The provided job ID is sent to an external AICNIC endpoint over plain HTTP. <br>
Mitigation: Use the skill only when the user intends to query AICNIC, and avoid submitting sensitive job IDs unless the user accepts that network exposure. <br>
Risk: Unusual jobId values can create request or shell-command handling issues when interpolated into a URL or curl command. <br>
Mitigation: Validate or URL-encode jobId values and prefer a safe HTTP client over direct shell interpolation. <br>


## Reference(s): <br>
- [AICNIC job status API endpoint](http://www.aicnic.cn/jobs/api/jobs/infos/hpcai28/{jobId}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text with optional curl command and extracted JSON fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided jobId and an outbound request to the AICNIC job information endpoint.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

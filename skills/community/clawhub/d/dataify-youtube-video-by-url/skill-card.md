## Description: <br>
Submits YouTube video file collection jobs to Dataify Builder by URL and returns the created task ID and status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit Dataify Builder jobs that collect YouTube video files by URL and receive the resulting task_id and status. It also guides API TOKEN setup, parameter confirmation, and validation before submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill submits Dataify Builder jobs using the user's Dataify API TOKEN. <br>
Mitigation: Review all submitted parameters before execution and install only when Dataify Builder submissions are intended. <br>
Risk: Persisting DATAIFY_API_TOKEN can allow future sessions to reuse the token. <br>
Mitigation: Avoid saving DATAIFY_API_TOKEN persistently unless future session reuse is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-youtube-video-by-url) <br>
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify login](https://dashboard.dataify.com/login?utm_source=skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, JSON] <br>
**Output Format:** [Markdown guidance with optional shell commands and JSON task summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns Dataify task_id/status after Builder submission; does not retrieve video files.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

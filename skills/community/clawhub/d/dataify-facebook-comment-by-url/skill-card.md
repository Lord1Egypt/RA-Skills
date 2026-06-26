## Description: <br>
Submits Dataify Builder jobs that collect Facebook post comments by post URL and returns the resulting task ID and status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure and submit Dataify Builder tasks for collecting comments from one or more Facebook post URLs, then receive the Dataify task ID and status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Dataify API TOKEN authorizes submission of Facebook comment collection jobs to Dataify. <br>
Mitigation: Review submitted parameters before approval, provide the token only when needed, and avoid persistent local token storage unless the environment is trusted. <br>
Risk: Incorrect URLs or parameter values can submit an unintended collection job. <br>
Mitigation: Confirm the parameter table before submission and rely on the skill's validation for Facebook URL prefix, dropdown values, non-negative limits, and non-empty file names. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-facebook-comment-by-url) <br>
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify login](https://dashboard.dataify.com/login?utm_source=skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance, JSON] <br>
**Output Format:** [Markdown parameter tables and shell commands; the helper script prints a JSON task summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns task_id, status, submitted parameters, file_name, dashboard_url, and a completion message after successful Builder submission.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

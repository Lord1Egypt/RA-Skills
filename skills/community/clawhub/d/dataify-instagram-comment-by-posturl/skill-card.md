## Description: <br>
Submits Dataify Builder tasks that collect Instagram post comments by post URL and returns the created task ID and status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure and submit Dataify Instagram comment collection jobs for one or more Instagram post URLs, then receive the resulting task ID, status, and dashboard guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a saved Dataify token to launch real Instagram comment collection jobs. <br>
Mitigation: Install and run it only when that behavior is intended, and confirm which DATAIFY_API_TOKEN will be used before submission. <br>
Risk: A job may be submitted for an unintended Instagram post URL, including the documented default URL. <br>
Mitigation: Review the parameter table before each run and verify the exact Instagram URL before allowing the task to proceed. <br>
Risk: Dataify may charge for submitted jobs or enforce account limits. <br>
Mitigation: Confirm Dataify account limits or charges before execution and prefer a revocable scoped token. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-instagram-comment-by-posturl) <br>
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify login](https://dashboard.dataify.com/login?utm_source=skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions and parameter tables, shell command examples, and JSON task summaries from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script reports spider_id, task_id, status, submitted parameters, file_name, dashboard_url, and a message after successful submission.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

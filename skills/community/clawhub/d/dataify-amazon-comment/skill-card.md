## Description: <br>
Submits Dataify Builder tasks that collect Amazon product reviews by URL and returns the created task ID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit Amazon product review collection jobs through Dataify Builder, confirm the task parameters, and receive the resulting task_id for follow-up in Dataify. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends an Amazon product URL and an API-authenticated request to Dataify. <br>
Mitigation: Review the submitted URL before execution and use the skill only when sending the request to Dataify is acceptable. <br>
Risk: DATAIFY_API_TOKEN is a credential that may be exposed if stored or shared carelessly. <br>
Mitigation: Store the token only in trusted environments, avoid sharing sessions with untrusted users, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify Builder endpoint](https://scraperapi.dataify.com/builder) <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-amazon-comment) <br>
- [Publisher profile](https://clawhub.ai/user/dataify-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions and JSON task submission summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script prints task_id, url, file_name, dashboard_url, and message after a successful Dataify Builder submission.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Submits Amazon global product collection tasks to Dataify Builder by product URL, category URL, keyword, or keyword and brand, then returns the task ID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create Dataify Builder jobs for Amazon global product collection and retrieve the resulting task ID for follow-up in Dataify. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided Amazon URLs, keywords, brands, and collection options to Dataify. <br>
Mitigation: Review the parameter confirmation table before submission and change or remove any values that should not be sent. <br>
Risk: DATAIFY_API_TOKEN is a sensitive credential required for Builder requests. <br>
Mitigation: Treat the token as secret, prefer a scoped token if available, and avoid exposing it in shared prompts, logs, or command history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-amazon-global-product) <br>
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance and parameter tables with shell command examples; the helper script prints a JSON task summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful submissions return a task_id, submitted parameter summary, dashboard_url, and message.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

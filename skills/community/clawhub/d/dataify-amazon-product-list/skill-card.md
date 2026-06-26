## Description: <br>
Submits Amazon product list collection jobs by keyword and domain through Dataify Builder and returns the resulting task ID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create Dataify Builder jobs for Amazon product list collection, confirm submission parameters, and retrieve the task_id for later result management in Dataify. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a long-lived Dataify API TOKEN and sends submitted keyword, domain, page count, and file-name values to Dataify Builder. <br>
Mitigation: Confirm the submission parameters before running, avoid private or sensitive business queries unless appropriate, and store DATAIFY_API_TOKEN only in an approved local environment. <br>
Risk: A missing or invalid token, incorrect Builder identifiers, or invalid input values can cause the submission to fail or return no task_id. <br>
Mitigation: Validate required fields and page count, use the provided script where possible, and surface Builder errors without inventing result fields. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-amazon-product-list) <br>
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with parameter tables, shell commands, and JSON task summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns task_id, submitted parameter values, dashboard_url, and status or troubleshooting messages.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

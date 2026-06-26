## Description: <br>
Submit Dataify Amazon product collection tasks through Dataify Builder for ASINs, product URLs, keywords, category URLs, and Best Sellers URLs, then return the created task_id. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit Amazon product collection jobs to Dataify Builder, confirm task parameters, manage the Dataify API TOKEN, and receive the resulting task_id for later review in Dataify. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill submits jobs to an external Dataify Builder service using a Dataify API TOKEN. <br>
Mitigation: Require the token before submission, keep it in DATAIFY_API_TOKEN or explicit runtime input, and review the task parameters before the Builder request is made. <br>
Risk: Incorrect ASINs, URLs, zip codes, page counts, price ranges, or sort options can create failed or unintended collection tasks. <br>
Mitigation: Normalize and validate mode-specific parameters, show submitted values in a Markdown table, and ask the user whether values should change before submission. <br>
Risk: Users may expect downloaded result files after submitting a task. <br>
Mitigation: Stop after successful Builder submission and direct the user to Dataify with the returned task_id to view or manage results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-amazon-product) <br>
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with parameter tables and optional shell commands; successful script submissions print JSON containing task_id, submitted parameters, dashboard_url, and message.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stops after task submission and does not download result files. Requires a Dataify API TOKEN before calling Builder.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

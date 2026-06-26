## Description: <br>
Submits Dataify Walmart Product Information Builder tasks for product collection by URL, category URL, SKU, or keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure and submit Walmart product collection jobs through Dataify, then receive the resulting task ID and status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill submits Walmart collection tasks to Dataify and may consume quota or send unintended URLs, SKUs, or keywords if triggered too broadly. <br>
Mitigation: Review the exact collection mode and parameters with the user and require clear confirmation before creating a Builder task. <br>
Risk: Dataify API tokens are required for submission and could be exposed if handled casually. <br>
Mitigation: Keep API tokens private, prefer the DATAIFY_API_TOKEN environment variable for local reuse, and do not persist tokens without explicit user confirmation. <br>
Risk: Inputs outside the intended Walmart domain or empty required values can create failed or unintended collection tasks. <br>
Mitigation: Validate Walmart URLs, domain, mode, SKU, keyword, page limits, variation flags, and file name before submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-walmart-products) <br>
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify login](https://dashboard.dataify.com/login?utm_source=skill) <br>
- [Dataify Builder endpoint](https://scraperapi.dataify.com/builder?platform=1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and JSON task-submission results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful submissions return a Dataify task_id, status, parameters, file_name, dashboard_url, and message.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

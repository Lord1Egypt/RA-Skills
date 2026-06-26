## Description: <br>
Submit Dataify eBay Product Information Builder tasks for eBay product collection by product URL, category URL, keyword, or store URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and e-commerce data users use this skill to submit guided Dataify Builder jobs that collect eBay product information and return a task ID and status for result tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Dataify API TOKEN is sensitive. <br>
Mitigation: Keep DATAIFY_API_TOKEN private, do not call the Builder endpoint without a token, and only save a token locally after user confirmation. <br>
Risk: Submitted URLs or keywords are sent to Dataify and may consume the user's Dataify account quota. <br>
Mitigation: Review the selected collection mode and parameters before submitting a Builder job. <br>
Risk: Incorrect mode or parameter values can create an unintended eBay collection task. <br>
Mitigation: Validate the selected mode, eBay URL domain, keyword, count values, and file name before submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-ebay-products) <br>
- [Publisher profile](https://clawhub.ai/user/dataify-server) <br>
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify login](https://dashboard.dataify.com/login?utm_source=skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with optional shell commands and JSON task submission summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Dataify Builder task details including mode, spider_id, task_id, status, parameters, file_name, dashboard_url, and message when the helper script succeeds.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

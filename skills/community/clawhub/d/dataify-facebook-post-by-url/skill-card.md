## Description: <br>
Submit Dataify Facebook post collection jobs by post URL through Dataify Builder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit one or more Facebook post URLs to Dataify Builder and receive a task_id, status, and dashboard link for results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Facebook post URLs and a Dataify API token to Dataify. <br>
Mitigation: Use it only when that data transfer is acceptable, keep the API TOKEN out of shared logs, and rely on DATAIFY_API_TOKEN or explicit per-run input instead of embedding secrets. <br>
Risk: The default target URL and broad invocation behavior can lead to unintended external collection jobs. <br>
Mitigation: Require an explicit user-provided Facebook post URL and confirm submitted parameters before creating a Dataify Builder task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-facebook-post-by-url) <br>
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify login](https://dashboard.dataify.com/login?utm_source=skill) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown responses with optional shell commands and JSON task summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful submissions may include task_id, status, submitted parameters, file_name, and dashboard URL.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

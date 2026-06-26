## Description: <br>
Submit Dataify YouTube comment collection tasks by video ID through Dataify Builder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit Dataify Builder jobs that collect YouTube comments for one or more video IDs and return the created task ID and status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Dataify API TOKEN and sends task parameters to Dataify. <br>
Mitigation: Use a dedicated token when possible, review the parameter table before submission, and proceed only when the user is comfortable using Dataify for YouTube comment collection. <br>
Risk: Persisting DATAIFY_API_TOKEN can allow future runs to use the token without re-entering it. <br>
Mitigation: Do not save DATAIFY_API_TOKEN persistently unless the user explicitly wants future runs to reuse it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dataify-server/dataify-youtube-comment-by-id) <br>
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify Login](https://dashboard.dataify.com/login?utm_source=skill) <br>
- [Dataify Builder Endpoint](https://scraperapi.dataify.com/builder?platform=1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API Calls, JSON] <br>
**Output Format:** [Markdown parameter confirmation and guidance, with JSON summaries from the helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns task_id, status, submitted parameters, file_name, dashboard_url, and message after successful submission; does not retrieve YouTube comments.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

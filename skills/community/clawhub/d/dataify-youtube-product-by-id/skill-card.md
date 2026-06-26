## Description: <br>
Submit Dataify Builder tasks that collect YouTube video basic information by video ID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit Dataify YouTube video basic information collection jobs for one or more YouTube video IDs and receive the Builder task ID and status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad invocation triggers could cause a saved Dataify API TOKEN to be used for an external YouTube data collection job when user intent is ambiguous. <br>
Mitigation: Use prompts that explicitly name Dataify and the target video ID, show the submitted parameters, and confirm before submitting a task or troubleshooting token access. <br>
Risk: The skill submits jobs to an external Dataify service and does not return collected YouTube data directly. <br>
Mitigation: Present the result as a Builder task submission, return only the task_id and status, and direct the user to Dataify to view or manage results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-youtube-product-by-id) <br>
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify Login](https://dashboard.dataify.com/login?utm_source=skill) <br>
- [Dataify Builder API endpoint](https://scraperapi.dataify.com/builder?platform=1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown parameter tables, shell commands, and JSON task summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Dataify API TOKEN; returns task_id, status, submitted parameters, dashboard URL, and guidance rather than collected YouTube data.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Guides an agent through Dataify Builder submissions for YouTube profile collection by URL or keyword, returning task IDs and statuses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit Dataify Builder jobs that collect YouTube channel profile data from specific URLs or search keywords, then receive task metadata for follow-up in Dataify. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be invoked implicitly for YouTube profile collection requests. <br>
Mitigation: Install it only when Dataify YouTube profile collection is intended, and confirm the selected mode, targets, and parameters before submission. <br>
Risk: The skill can reuse a saved DATAIFY_API_TOKEN to submit Dataify Builder jobs. <br>
Mitigation: Keep the token scoped and rotatable, avoid sharing it in prompts when possible, and remove or rotate it when access is no longer needed. <br>
Risk: Submitted jobs may collect data from unintended YouTube URLs or keywords. <br>
Mitigation: Review URL or keyword inputs, page counts, and file names before running the Builder request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-youtube-profiles) <br>
- [Publisher profile](https://clawhub.ai/user/dataify-server) <br>
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with optional shell commands and JSON task summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns Dataify task_id, status, selected mode, submitted parameters, file name, dashboard URL, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

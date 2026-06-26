## Description: <br>
Submit Dataify Reddit Post Information Builder tasks for Reddit post collection by post URL, keyword, or subreddit URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure and submit Dataify Builder jobs that collect Reddit posts by post URL, search keyword, or subreddit URL, then receive the returned task ID and status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API TOKEN exposure during setup or task submission. <br>
Mitigation: Prefer the DATAIFY_API_TOKEN environment variable for reuse, avoid pasting tokens into chat when possible, and do not persist tokens without explicit user confirmation. <br>
Risk: Unintended Reddit collection jobs can be submitted if the mode or parameters are wrong. <br>
Mitigation: Review the selected mode, URLs or keywords, post count, sort options, and file name before approving submission; the helper script validates supported modes, Reddit URL prefixes, non-negative counts, and allowed sort choices. <br>
Risk: The skill sends chosen Reddit collection parameters to Dataify's Builder service. <br>
Mitigation: Use the skill only when the user intends to create Dataify Reddit collection jobs, require an API TOKEN before submission, and direct users to the Dataify dashboard to view or manage results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-reddit-posts) <br>
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify login](https://dashboard.dataify.com/login?utm_source=skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with command examples; the helper script prints JSON after successful task submission.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful submissions include mode, spider_id, task_id, status, submitted parameters, file_name, dashboard_url, and message.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

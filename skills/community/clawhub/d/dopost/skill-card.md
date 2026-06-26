## Description: <br>
Use the Dopost REST API to publish, schedule, and manage social media posts programmatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dopost](https://clawhub.ai/user/dopost) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to help an agent call the Dopost REST API for social account lookup, media upload, post publishing, scheduling, status checks, rescheduling, and deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to publish, schedule, reschedule, upload media for, or delete social posts through a Dopost API key. <br>
Mitigation: Require explicit user confirmation before publishing immediately, scheduling, rescheduling, uploading media, or deleting any post or media item. <br>
Risk: A Dopost API key could grant broad access to connected social accounts. <br>
Mitigation: Use the most limited Dopost API key available and keep it out of committed files. <br>


## Reference(s): <br>
- [Dopost API documentation](https://dopost.co/docs/api) <br>
- [ClawHub skill page](https://clawhub.ai/dopost/dopost) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a DOPOST_API_KEY environment variable for authenticated Dopost API requests.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

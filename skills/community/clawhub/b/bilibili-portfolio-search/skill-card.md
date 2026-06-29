## Description: <br>
Queries a Bilibili creator's public video portfolio by UID, sorts returned works by play count, and supports cursor-based pagination for additional results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, MCN operations teams, content researchers, and Bilibili viewers use this skill to inspect a creator's public upload portfolio, identify high-performing videos, and page through more works by UID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key for access. <br>
Mitigation: Treat REDFOX_API_KEY as a secret, keep it out of chats, code, logs, and output files, and rotate or revoke it if exposed. <br>
Risk: Queried Bilibili UIDs are sent to RedFox for lookup. <br>
Mitigation: Use the skill only when sending the target UID to RedFox is acceptable for the user's workflow. <br>
Risk: The helper script makes live network requests and may fail on invalid credentials, API errors, or network timeouts. <br>
Mitigation: Confirm the API key is configured, review error output, and retry only when the failure is transient. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/bilibili-portfolio-search) <br>
- [RedFox publisher profile](https://clawhub.ai/user/redfox-data) <br>
- [Core workflow](references/core_workflow.md) <br>
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables and short status text, with helper-script JSON used by the agent before presentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Bilibili UID and REDFOX_API_KEY; supports an optional cursor for pagination.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

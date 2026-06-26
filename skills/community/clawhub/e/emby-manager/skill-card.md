## Description: <br>
Manages an Emby media server on a Linux NAS, including media library operations, metadata refreshes, playback history, user permissions, and server health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gmd170629](https://clawhub.ai/user/gmd170629) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and media server administrators use this skill to operate Emby instances through guided API calls, structured status reports, user and permission checks, media-library maintenance, and troubleshooting steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Emby API-key access can allow administrative actions or data access beyond the immediate request. <br>
Mitigation: Use a limited or temporary API key when possible, paste it only when needed, and rotate it after use. <br>
Risk: Server, user, viewing-history, IP address, and log data may be exposed in agent responses. <br>
Mitigation: Share only the records needed for the task and redact sensitive user, IP, or log details before broader distribution. <br>
Risk: Delete, restart, scan, and permission-change operations can affect server availability or media access. <br>
Mitigation: Confirm these actions with the user before execution and state the expected impact before proceeding. <br>


## Reference(s): <br>
- [Emby API Quick Reference](references/api-guide.md) <br>
- [Media Library Operations Guide](references/media-ops.md) <br>
- [Emby Troubleshooting Guide](references/troubleshoot.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, structured lists, inline API examples, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided Emby server URL and API key; destructive or disruptive actions should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

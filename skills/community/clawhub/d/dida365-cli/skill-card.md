## Description: <br>
Helps agents use the Dida365 Node.js CLI to manage tasks, projects, tags, completed-task queries, synchronization, and batch operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oymy](https://clawhub.ai/user/oymy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation-focused Dida365 users can use this skill to have an agent prepare CLI commands for account authentication, project and task management, tag operations, completed-task queries, synchronization, and batch changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI requires a raw Dida365 session cookie, which can expose account access if copied into shared shells, logs, or untrusted environments. <br>
Mitigation: Use the cookie only in trusted local or controlled agent environments, avoid echoing it into logs, and rotate the cookie if exposure is suspected. <br>
Risk: The CLI can read, edit, move, merge, and delete Dida365 account data through external npm code. <br>
Mitigation: Verify the npm package and version before installation, review proposed commands before execution, and require explicit confirmation before delete, merge, move, or batch operations. <br>
Risk: The documented private Dida365 API endpoints are unofficial and may change without notice. <br>
Mitigation: Test commands on low-risk tasks first and review command output before relying on the workflow for important automation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oymy/dida365-cli) <br>
- [Dida365 Open API](https://developer.dida365.com/) <br>
- [Dida365 API Base Endpoint](https://api.dida365.com/api/v2) <br>
- [ticktick-py Private API Reference](https://github.com/lazeroffmichael/ticktick-py) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may interact with a live Dida365 account and require cookie authentication.] <br>

## Skill Version(s): <br>
3.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

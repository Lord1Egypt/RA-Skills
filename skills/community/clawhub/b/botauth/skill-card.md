## Description: <br>
Use the botauth CLI to list, search, and retrieve secrets from the user's unlocked botauth vault with per-request approval in the desktop app. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EYHN](https://clawhub.ai/user/EYHN) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when a task needs API keys, tokens, or passwords already stored in a local botauth vault. It supports listing, searching, retrieving, and user-mediated creation flows while keeping desktop approval in the loop. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent request credentials from a local vault, so overly broad approval or unnecessary retrieval may expose secrets beyond the current task. <br>
Mitigation: Install only when the botauth CLI is trusted, keep the vault locked when not needed, approve only task-specific prompts, and reuse short-lived access keys only within the active workflow. <br>
Risk: Secrets written into long-lived files such as environment files or configuration can persist after the immediate task. <br>
Mitigation: Avoid writing sensitive values into durable files unless the task clearly requires it, and review any generated configuration before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EYHN/botauth) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference short-lived access keys and sensitive values returned by approved botauth CLI requests.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

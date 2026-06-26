## Description: <br>
Manage grocery and shopping lists via AnyList. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjrussell](https://clawhub.ai/user/mjrussell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to inspect, add, check, uncheck, remove, and clear grocery or shopping-list items through the AnyList CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify or clear shopping-list data once configured. <br>
Mitigation: Tell the agent to ask before removing or clearing list items, and review proposed list changes before execution. <br>
Risk: The skill requires AnyList account access through anylist-cli. <br>
Mitigation: Keep credentials in environment variables, avoid exposing them in prompts or logs, and review the CLI package if it is not already trusted. <br>


## Reference(s): <br>
- [AnyList](https://www.anylist.com) <br>
- [ClawHub Anylist Skill](https://clawhub.ai/mjrussell/anylist) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the anylist CLI and an authenticated AnyList account; some commands can modify list data.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

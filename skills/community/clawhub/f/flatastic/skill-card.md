## Description: <br>
Manage shared household chores, shopping lists, expenses, and household messages via the Flatastic CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[david-schopf](https://clawhub.ai/user/david-schopf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and household members use this skill to ask an agent for Flatastic CLI commands and guidance for chores, shopping lists, expenses, balances, WG information, and shared household messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be invoked too broadly and cause an agent to read or change shared household chores, shopping items, expenses, members, or account data. <br>
Mitigation: Invoke it only when the user explicitly mentions Flatastic or asks to read or update household records. <br>
Risk: Mutating Flatastic actions can create, edit, delete, or notify household members about shared records. <br>
Mitigation: Require user confirmation before creating, editing, deleting, or sending reminder actions. <br>


## Reference(s): <br>
- [ClawHub Flatastic skill page](https://clawhub.ai/david-schopf/flatastic) <br>
- [david-schopf publisher profile](https://clawhub.ai/user/david-schopf) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Flatastic CLI commands that read or modify shared household data.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

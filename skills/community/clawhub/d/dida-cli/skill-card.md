## Description: <br>
Manage tasks and projects in 滴答清单 for task, to-do, reminder, and event workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ilooch](https://clawhub.ai/user/ilooch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to install and authenticate the Dida CLI, then manage Dida projects and tasks with cautious selection, confirmation, and summary workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a Dida account through OAuth PKCE or an API token. <br>
Mitigation: Install and authenticate only when the user trusts @suibiji/dida-cli; prefer the browser OAuth flow over pasting an API token. <br>
Risk: Task-changing commands can update, complete, move, or delete user tasks. <br>
Mitigation: Review selected projects and tasks before changes, and require explicit confirmation before delete or bulk cleanup commands. <br>


## Reference(s): <br>
- [Dida homepage](https://dida365.com) <br>
- [ClawHub skill page](https://clawhub.ai/ilooch/dida-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the dida CLI and Dida account authentication through OAuth PKCE or an API token.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

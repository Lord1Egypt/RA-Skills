## Description: <br>
Manage Apple Reminders on macOS through the `remindctl` CLI for listing, adding, editing, completing, and deleting reminders with list filters, date filters, and JSON or plain output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers on macOS use this skill to ask an agent for `remindctl` commands and guidance that view, create, update, complete, and delete Apple Reminders and lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to run `remindctl` commands that edit, complete, rename, or delete reminders and lists, including commands using `--force`. <br>
Mitigation: Confirm reminder-changing commands with the user before execution, especially edit, complete, rename, delete, and any `--force` command. <br>
Risk: The skill depends on macOS Reminders permissions and a third-party `remindctl` Homebrew tap. <br>
Mitigation: Install only when the user trusts the documented tap, verify `remindctl` is available, and grant Reminders access only on the Mac where commands will run. <br>


## Reference(s): <br>
- [Apple Reminders ClawHub release](https://clawhub.ai/steipete/apple-reminders) <br>
- [remindctl project homepage](https://github.com/steipete/remindctl) <br>
- [Publisher profile](https://clawhub.ai/user/steipete) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that read or modify Apple Reminders through `remindctl`; JSON, plain, or quiet output flags may be suggested for scripting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

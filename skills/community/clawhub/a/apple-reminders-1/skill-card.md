## Description: <br>
Manage Apple Reminders via the `remindctl` CLI on macOS (list, add, edit, complete, delete). Supports lists, date filters, and JSON/plain output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tigertamvip](https://clawhub.ai/user/tigertamvip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users on macOS use this skill to have an agent operate Apple Reminders through the local `remindctl` CLI, including viewing, creating, editing, completing, and deleting reminders and lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide commands that complete, rename, or delete reminders and lists. <br>
Mitigation: Review destructive `remindctl` commands before running them, especially delete, complete, and list rename operations. <br>
Risk: The skill depends on a local third-party CLI and Homebrew tap to access Apple Reminders. <br>
Mitigation: Install only if you trust the `remindctl` Homebrew tap or source project, and grant Reminders permission only on the Mac where the CLI is intended to run. <br>


## Reference(s): <br>
- [remindctl project homepage](https://github.com/steipete/remindctl) <br>
- [ClawHub skill page](https://clawhub.ai/tigertamvip/apple-reminders-1) <br>
- [Publisher profile](https://clawhub.ai/user/tigertamvip) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can guide JSON, plain TSV, and quiet count output modes supported by `remindctl`.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

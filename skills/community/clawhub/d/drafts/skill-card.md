## Description: <br>
Manage Drafts app notes through a macOS CLI that can create, view, list, edit, append, prepend, and run actions on drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nerveband](https://clawhub.ai/user/nerveband) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, employees, and external users on macOS use this skill to manage Drafts notes from an agent workflow, including capture, lookup, updates, and Drafts action execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external Drafts CLI and local macOS automation. <br>
Mitigation: Install it only on macOS systems that use Drafts, review or pin the CLI before use, and keep Drafts running when executing commands. <br>
Risk: Commands that replace note contents or run Drafts actions can permanently change Drafts data. <br>
Mitigation: Review destructive commands before execution and confirm the target draft UUID or action name. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nerveband/drafts) <br>
- [Drafts CLI homepage](https://github.com/nerveband/drafts) <br>
- [Drafts app](https://getdrafts.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Text, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Drafts CLI JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS, the Drafts app running, Drafts Pro for automation features, and the drafts CLI binary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

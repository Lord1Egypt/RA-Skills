## Description: <br>
Manage Apple Notes through the memo CLI on macOS to create, view, edit, delete, search, move, and export notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangfeng1995](https://clawhub.ai/user/huangfeng1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
macOS users and their agents use this skill to manage Apple Notes from the terminal through the memo CLI, including note creation, search, folder moves, deletion, and HTML or Markdown export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change Apple Notes when requested. <br>
Mitigation: Install only if you are comfortable giving the memo CLI and your agent access to Apple Notes, and review selected notes before edit, move, delete, or export actions. <br>
Risk: macOS Automation access may remain available after the skill is no longer needed. <br>
Mitigation: Revoke the memo CLI or agent Automation permission in macOS privacy settings when you no longer use the skill. <br>


## Reference(s): <br>
- [Apple Notes.Old on ClawHub](https://clawhub.ai/huangfeng1995/apple-notes-old) <br>
- [memo CLI homepage from skill metadata](https://github.com/antoniorodr/memo) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS, Apple Notes.app access, and the memo CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

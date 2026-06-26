## Description: <br>
Manage Apple Notes through the memo CLI on macOS, including creating, viewing, editing, deleting, searching, moving, and exporting notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage local Apple Notes from an agent-assisted macOS terminal workflow while preserving confirmation and privacy guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a third-party memo CLI with access to Apple Notes. <br>
Mitigation: Install only if the memo CLI is trusted and grant Apple Notes Automation permissions intentionally. <br>
Risk: Note contents may include private information that should not leave the local machine. <br>
Mitigation: Do not pipe or redirect note contents to network-transmitting commands, APIs, or remote services. <br>
Risk: Deletion and bulk move operations can change or remove user notes. <br>
Mitigation: Review the exact note or folder scope before acting, require user confirmation, and handle deletion of named notes one at a time. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/snazar-faberlens/apple-notes-hardened) <br>
- [Publisher Profile](https://clawhub.ai/user/snazar-faberlens) <br>
- [memo CLI](https://github.com/antoniorodr/memo) <br>
- [Faberlens Apple Notes Safety Evaluation](https://faberlens.ai/explore/apple-notes) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [macOS-only; requires the memo CLI, Apple Notes.app, and local Automation permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Manage Apple Reminders via the `remindctl` CLI on macOS (list, add, edit, complete, delete). Supports lists, date filters, and JSON/plain output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill on macOS to inspect and manage Apple Reminders from an agent workflow while keeping reminder access scoped to the requested task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify personal reminder data. <br>
Mitigation: Install only when the remindctl source is trusted, grant macOS Reminders access intentionally, and scope reads to the user's requested list or date range. <br>
Risk: Edits, completions, renames, and deletes can affect the wrong reminders if the target is ambiguous. <br>
Mitigation: Confirm exact reminder IDs, list names, or titles before state-changing operations. <br>
Risk: Reminder contents may expose private schedule or note information if sent to external services. <br>
Mitigation: Keep reminder output local and do not pipe it to network-transmitting commands or webhooks. <br>


## Reference(s): <br>
- [Apple Reminders Hardened on ClawHub](https://clawhub.ai/snazar-faberlens/apple-reminders-hardened) <br>
- [remindctl project](https://github.com/steipete/remindctl) <br>
- [Faberlens safety evaluation](https://faberlens.ai/explore/apple-reminders) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON/plain CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local remindctl command guidance for macOS; JSON and plain output are available when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

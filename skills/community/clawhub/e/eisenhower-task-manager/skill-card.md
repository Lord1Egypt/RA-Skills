## Description: <br>
Task management based on Eisenhower Matrix and P0-P2 priority with customer project management, four execution quadrants, and a separate customer project list for all customer work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yayayahei](https://clawhub.ai/user/yayayahei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and individual operators use this skill to organize personal execution tasks, customer projects, delegated work, and future ideas in markdown-backed Eisenhower Matrix lists. It can also launch a local real-time dashboard for visual review and direct task updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dashboard includes a browser-accessible terminal that can run a real shell. <br>
Mitigation: Use the dashboard only on a trusted machine, keep it bound to local-only access, do not expose the port to a network, and treat terminal access as equivalent to command-line access to the user account. <br>
Risk: Daemon mode keeps the dashboard and terminal session running after the launching terminal closes. <br>
Mitigation: Use daemon mode only when persistence is needed, track the selected port and PID, and stop the service when the dashboard is no longer in use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yayayahei/eisenhower-task-manager) <br>
- [Repository Link Declared by Skill](https://github.com/yayayahei/skills/tree/main/eisenhower-task-manager) <br>
- [Task Addition Flow](references/task-add.md) <br>
- [Task Completion Flow](references/task-complete.md) <br>
- [Numbering Rules](references/numbering-rules.md) <br>
- [Dashboard Offer Workflow](references/dashboard-offer.md) <br>
- [Dashboard README](dashboard/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown task updates, markdown file edits, and optional shell commands for the local dashboard] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local markdown task files and may offer to start a local web dashboard after task operations.] <br>

## Skill Version(s): <br>
8.3.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

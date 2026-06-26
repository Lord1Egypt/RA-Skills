## Description: <br>
General AI agent introspection debugging framework: auto capture errors, root cause analysis, automatic repair, fix verification, no manual intervention required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benxiao2026](https://clawhub.ai/user/benxiao2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture runtime errors, analyze likely root causes, propose or apply repairs, and verify whether an agent workflow recovered successfully. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic repair workflows can make host-level changes, including package installs, service restarts, cache deletion, and configuration edits. <br>
Mitigation: Disable automatic fixes by default and require explicit review or confirmation before applying changes. <br>
Risk: Captured error logs and tracebacks can contain sensitive data from the failing workflow. <br>
Mitigation: Treat diagnostic logs as sensitive, restrict access, and avoid sharing them outside the trusted workspace. <br>
Risk: Generated fixes can be incorrect or broader than intended. <br>
Mitigation: Constrain repairs to the intended workspace, back up changed files, scan changes, and verify behavior before deployment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python, shell, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose package installs, service restarts, cache deletion, config edits, and diagnostic logging depending on the repair path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

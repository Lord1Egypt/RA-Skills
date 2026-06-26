## Description: <br>
Bridge any AI coding agent to Antigravity executors for task dispatch, receipt tracking, stuck detection, and continue/approve/reject/retry flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[logicrw](https://clawhub.ai/user/logicrw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to delegate coding work to Antigravity through the agpair CLI, monitor health and task state, review evidence, and choose a single follow-up action such as continue, approve, reject, or retry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated task state or logs may be misread, leading to premature completion claims or an inappropriate continue, approve, reject, or retry action. <br>
Mitigation: Check doctor and daemon health, current task status, latest logs, and active waits before acting; require human confirmation for approvals, retries, or force-like recovery on important repositories. <br>
Risk: The workflow depends on the agpair CLI and Antigravity executor being intentionally installed and trusted. <br>
Mitigation: Install only when agpair and the executor are expected in the environment, use explicit requests such as "use agpair," and review logs and evidence before taking action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/logicrw/agpair) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/logicrw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no bundled code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

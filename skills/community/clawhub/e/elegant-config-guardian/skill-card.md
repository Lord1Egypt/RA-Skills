## Description: <br>
Safely applies OpenClaw config changes with automatic rollback and an ack timeout guard for risky runtime configuration changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangwu-30](https://clawhub.ai/user/wangwu-30) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to apply OpenClaw runtime configuration changes with backup, restart, health-check, optional manual acknowledgement, and rollback behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The apply command can execute arbitrary shell supplied through --apply-cmd. <br>
Mitigation: Only pass reviewed, deterministic commands from trusted sources, and never build the command from untrusted text. <br>
Risk: Rollback restores the target config file but may not undo side effects outside that file. <br>
Mitigation: Validate the proposed command's side effects before execution and require explicit acknowledgement only after end-to-end checks pass. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangwu-30/elegant-config-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command-oriented guidance for guarded config application; no structured machine output is declared.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

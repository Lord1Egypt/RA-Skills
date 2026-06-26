## Description: <br>
System safety and control-plane skill that helps prevent agent deadlocks and freezes by providing non-LLM controls to inspect task state, flush message queues, cancel long-running work, and recover without restarting the container. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Amar1432](https://clawhub.ai/user/Amar1432) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to add emergency control-plane commands and watchdog behavior for long-running or high-risk OpenClaw workloads. It is intended for advanced users who need to inspect task health, cancel stalled work, and recover from unresponsive agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Emergency control commands can terminate active work or exec sessions. <br>
Mitigation: Restrict who can invoke /flush and /recover, and verify whether process termination can affect unrelated sessions before enabling autonomous use. <br>
Risk: The sub-agent spawning helper may create additional sessions with limited scoping or confirmation. <br>
Mitigation: Review or disable the spawning helper unless isolated sub-agent execution is required for the deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Amar1432/error-guard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with TypeScript helper modules and control command descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defines control-plane actions for status checks, flush, recovery, task heartbeat events, watchdog cancellation, and optional sub-agent spawning.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

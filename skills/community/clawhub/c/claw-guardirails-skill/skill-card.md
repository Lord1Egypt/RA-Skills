## Description: <br>
Enforces guarded execution with safe_exec, safe_send, and safe_action for shell commands, outbound messages, and external actions that can mutate data or state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eveiljuice](https://clawhub.ai/user/eveiljuice) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to route potentially risky command execution, outbound messaging, and external side-effect actions through approval-aware guarded tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill only reduces risk when the host environment provides and enforces safe_exec, safe_send, and safe_action. <br>
Mitigation: Deploy it only in agent runtimes where those guarded tools are available and direct execution, messaging, or external action paths cannot bypass policy. <br>
Risk: Unsafe requests may still require human approval or denial decisions. <br>
Mitigation: Stop when a guarded tool returns require_approval or deny, and continue only through the explicit approval flow described by the environment. <br>


## Reference(s): <br>
- [ClawGuardrails on ClawHub](https://clawhub.ai/eveiljuice/claw-guardirails-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with JSON tool input examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; it does not add code, persistence, credentials, or hidden behavior.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

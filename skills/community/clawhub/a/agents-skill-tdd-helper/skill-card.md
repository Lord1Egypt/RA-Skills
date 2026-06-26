## Description: <br>
Lightweight helper to enforce TDD-style loops for non-deterministic agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cerbug45](https://clawhub.ai/user/cerbug45) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to require a passing pytest-based test step before an agent runs a target command. It is suited for workflows where a test-first loop helps constrain non-deterministic code generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper can run raw shell commands supplied through --run, TEST_CMD, and LINT_CMD. <br>
Mitigation: Review command arguments and related environment variables before use, and avoid untrusted inputs in shared, CI, or agent-controlled environments. <br>
Risk: The security verdict is suspicious because local command execution occurs under the user's account. <br>
Mitigation: Install and run only in workspaces where local shell execution is acceptable, and review the skill before deployment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/cerbug45/agents-skill-tdd-helper) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command output with shell command execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs pytest against the configured test path before executing the requested command; optional lint execution is controlled by environment variables.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description:

Lightweight helper to enforce TDD-style loops for non-deterministic agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cerbug45](https://clawhub.ai/user/cerbug45)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to require passing tests before running an agent-generated command, with optional lint checks for warnings-as-errors workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper exposes broad shell command execution through --run, TEST_CMD, and LINT_CMD.

Mitigation: Install and invoke it only in trusted repositories, CI jobs, agent sessions, and environments; review command inputs before execution.

Risk: Shell-based command execution can treat trusted-code inputs as executable shell syntax rather than plain data.

Mitigation: A future safer version should call pytest and linters with structured argument lists and avoid shell=True for user-controlled values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cerbug45/skills/agents-skill-tdd-helper)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands and command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and pytest; optional lint enforcement uses WARN_AS_ERROR and LINT_CMD.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

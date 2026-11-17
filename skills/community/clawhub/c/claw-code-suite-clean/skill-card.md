## Description:

Claw Code Suite (Python-Only Edition) provides a local Python harness for routing, inspecting, and invoking Claw Code-inspired tools and commands for security analysis, code quality, development workflows, and agent orchestration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devita3323](https://clawhub.ai/user/devita3323)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run local harness commands, inspect routed tool and command metadata, and support code review, security analysis, and development workflow tasks in OpenClaw-style agent environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the release overstates its tool execution capabilities.

Mitigation: Validate required commands in a local sandbox before relying on the suite for production workflows.

Risk: The security review says raw prompts and outputs are stored in local logs by default.

Mitigation: Avoid submitting secrets or proprietary code unless event logging is disabled, redirected, or tightly access-controlled.

Risk: The security guidance flags Python, module, and session path handling as needing hardening before shared or sensitive use.

Mitigation: Run the skill in an isolated workspace and restrict writable paths when using it with untrusted inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/devita3323/skills/claw-code-suite-clean)
- [Claw Code project homepage](https://github.com/instructkr/claw-code)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text, Markdown, JSON, Python code snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command output may be time-limited and truncated according to local environment settings.]

## Skill Version(s):

1.0.1 (source: release evidence, CHANGELOG, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Provides guidance and example scripts for upgrading OpenClaw with Claude-Code-style concurrent execution, self-reflection, vector memory retrieval, sub-agent orchestration, and context compression.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smseow001](https://clawhub.ai/user/smseow001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill as implementation guidance for upgrading OpenClaw with concurrent task handling, memory retrieval, scheduled self-reflection, long-running health checks, and context compression.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent root-scoped automation and cron jobs can create privileged background behavior that users may not intend.

Mitigation: Review setup commands before use, avoid /root paths, and make scheduled jobs a separate explicit opt-in.

Risk: The proposed task executor can run broad shell commands without tight safeguards.

Mitigation: Replace shell-based execution with allowlisted commands, constrained arguments, timeouts, and explicit operator approval for high-impact actions.

Risk: Unpinned dependencies and npx @latest can change behavior between installs.

Mitigation: Pin package versions and verify dependencies before installation or execution.

Risk: Vector memory and reflection logs may retain sensitive agent context over time.

Mitigation: Define retention limits, deletion controls, and review procedures before enabling persistent memory.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/smseow001/skills/claude-code-engine)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are implementation guidance and example automation snippets for an agent to review before use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

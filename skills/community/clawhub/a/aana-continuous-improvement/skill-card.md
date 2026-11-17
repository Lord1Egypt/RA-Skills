## Description:

AANA-grounded continuous self-improvement instructions for OpenClaw-style agents, with explicit approval, memory, and scope boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this instruction-only skill to help agents review outcomes, identify small workflow improvements, and gate any future-facing changes through explicit user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Self-improvement suggestions could be applied beyond the current task or alter memory, files, tools, policies, permissions, or user expectations without approval.

Mitigation: Keep improvements inside the current task unless the user explicitly approves future behavior, persistence, files, tools, policy, permission, or scope changes.

Risk: Review payloads could expose secrets or unnecessary private content.

Mitigation: Use minimal redacted summaries and exclude access tokens, passwords, full payment data, unnecessary private records, and unrelated user messages.

Risk: Weak evidence could lead to misleading claims that an agent improved.

Mitigation: Separate observed outcomes from guesses, label uncertain improvements as hypotheses, and verify the next output against the original user request.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mindbomber/skills/aana-continuous-improvement)
- [README](artifact/README.md)
- [Improvement Cycle Schema](artifact/schemas/improvement-cycle.schema.json)
- [Redacted Improvement Cycle Example](artifact/examples/redacted-improvement-cycle.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown or short text reports with optional JSON review payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; optional review payloads should use redacted summaries and follow the bundled JSON schema.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact manifest reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

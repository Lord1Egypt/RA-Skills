## Description:

Expert code review for embedded/firmware projects with dual-model cross-review (Claude + Codex via ACP). Detects memory safety, interrupt hazards, RTOS pitfalls, hardware interface bugs, and C/C++ anti-patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ylongw](https://clawhub.ai/user/ylongw)

### License/Terms of Use:

MIT

## Use Case:

Developers and firmware engineers use this skill to review embedded C/C++ changes for memory safety, interrupt and RTOS correctness, hardware interface issues, security concerns, and maintainability. It supports single-model review for small diffs and dual-model cross-review for larger or critical firmware changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewed diffs may be shared with configured ACP agents.

Mitigation: Use the skill only with repositories and agents approved for the firmware source being reviewed.

Risk: The diff preparation script accepts an unvalidated diff range that could be abused to overwrite files writable by the agent user.

Mitigation: Reject ranges beginning with '-' and validate revisions before running the script, or run reviews in a limited sandbox.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ylongw/skills/embedded-review)
- [Understanding Agent Scaling in LLM-Based Multi-Agent Systems via Diversity](https://arxiv.org/abs/2602.03794)
- [Memory Safety Checklist](references/memory-safety.md)
- [Interrupt & Concurrency Safety Checklist](references/interrupt-safety.md)
- [Hardware Interface Checklist](references/hardware-interface.md)
- [C/C++ Pitfalls Checklist](references/c-pitfalls.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown review report with severity-ranked findings, cross-review analysis, hardware and timing concerns, architecture notes, and suggested fixes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands to prepare review diffs; dual-model mode depends on configured Claude Code and Codex agents.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

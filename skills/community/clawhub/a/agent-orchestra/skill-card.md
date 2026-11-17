## Description:

Design and compose multi-agent graphs for correctness, coverage, or creativity. Use when a task benefits from isolated proposals, explicit arbitration, adversarial verification, committees, recursive review, cross-modal checks, or saturation loops. Applies across agent runtimes; the included JavaScript workflow is one adapter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Agent Orchestra to choose and document collaboration graphs for uncertain design, correctness-critical implementation, research synthesis, artifact review, and iterative hardening. It helps define independent worker boundaries, arbitration, adversarial review, escalation, and integration evidence for multi-agent work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included workflow may fetch arbitrary URLs or render external content.

Mitigation: Restrict network access or allowlist trusted URL origins before running hosted workflows.

Risk: Fix mode can generate revised artifacts.

Mitigation: Use review mode by default and require explicit authorization before applying generated changes.

Risk: Coordinated agents may read repositories and produce patches.

Mitigation: Run in a disposable workspace without ambient browser credentials, treat agent output as untrusted input, and review patches before execution or integration.

Risk: The documented install command is unpinned.

Mitigation: Pin or verify the installation source before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antreasantoniou/skills/agent-orchestra)
- [SKILL.md](SKILL.md)
- [PLAYBOOK.md](PLAYBOOK.md)
- [Saturating review workflow example](examples/saturating-review-engine.workflow.js)
- [Token-efficient overlay](variants/token-efficient/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JavaScript workflow examples, shell commands, and structured review outputs when run by a compatible host]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill itself is runtime-neutral; outputs depend on the host agent runtime and may include graph plans, role briefs, review panels, dissent, gaps, patch proposals, or revised artifact manifests.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

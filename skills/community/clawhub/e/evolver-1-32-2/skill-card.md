## Description:

A self-evolution engine for AI agents that analyzes runtime history to identify improvements and applies protocol-constrained evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pppig1357](https://clawhub.ai/user/pppig1357)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent teams use this skill to inspect agent runtime history, extract signals, and produce GEP-guided evolution prompts, assets, and reviewable updates. It is intended for environments that need auditable, protocol-bound improvement cycles rather than free-form code changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote Hub content and automated loops can influence code changes and data sharing.

Mitigation: Install only in a disposable or tightly controlled repository, use review mode, and use only a trusted HTTPS A2A_HUB_URL.

Risk: Loop mode may expose private transcripts or secrets through outbound Hub sharing.

Mitigation: Do not run loop mode around private transcripts or secrets unless outbound sharing is acceptable.

Risk: Broad GitHub tokens can expand the impact of auto issue reporting or release actions.

Mitigation: Avoid providing broad GitHub tokens and scope any token to the minimum required permissions.

Risk: Rollback and self-modification behavior can affect repository state.

Mitigation: Prefer EVOLVER_ROLLBACK_MODE=stash, keep EVOLVE_ALLOW_SELF_MODIFY disabled unless explicitly needed, and review changes before applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pppig1357/skills/evolver-1-32-2)
- [EvoMap](https://evomap.ai)
- [EvoMap documentation](https://evomap.ai/wiki)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown/text guidance with JSON protocol assets and repository file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write GEP assets and memory files; source file updates are described as guarded by review, validation, and git controls.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact package version 1.32.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

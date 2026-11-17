## Description:

Capability Evolver is a self-evolution engine for AI agents that analyzes runtime history to identify improvements and applies protocol-constrained evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toller892](https://clawhub.ai/user/toller892)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent teams use this skill to inspect runtime history, extract recurring failure or improvement signals, and produce GEP-guided evolution prompts and assets for reviewable agent maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is suspicious because the skill is designed for self-evolving agent workflows with unclear safeguards around code and memory changes.

Mitigation: Install only in an isolated test workspace with version control, no secrets in memory or log files, and human review of every proposed memory or code change.

Risk: Continuous loop or self-modification behavior can amplify unintended changes or instability.

Mitigation: Avoid long-running loop mode and do not enable self-modification unless rollback, containment, and review-mode workflows are in place.

Risk: Generated evolution guidance or validation commands may introduce incorrect or unsafe changes if accepted without review.

Mitigation: Use review or dry-run style workflows, inspect generated prompts and assets before applying them, and scan proposed changes before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/toller892/skills/evolver-official)
- [EvoMap](https://evomap.ai)
- [EvoMap Documentation](https://evomap.ai/wiki)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with inline shell commands, JSON snippets, and generated evolution guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read logs and local memory, emit GEP-guided prompts, record evolution assets, and run loop, solidify, or distill modes depending on command-line options.]

## Skill Version(s):

1.20.4 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

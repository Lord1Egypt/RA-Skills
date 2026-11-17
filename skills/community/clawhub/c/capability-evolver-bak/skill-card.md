## Description:

A self-evolution engine for AI agents that analyzes runtime history, identifies improvements, and applies protocol-constrained evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samwlh](https://clawhub.ai/user/samwlh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent maintainers use this skill to inspect runtime history, select reusable evolution assets, and produce protocol-bound prompts or changes for repair, hardening, and improvement workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically modify code or memory during evolution workflows.

Mitigation: Run it in review mode, inspect diffs before solidifying changes, and keep Git backups for rollback.

Risk: The skill can contact external hubs and publish or fetch evolution assets.

Mitigation: Use a disposable or tightly sandboxed workspace and disable auto-publish, proactive Hub questions, and bridge execution unless explicitly needed.

Risk: Dependency auto-healing can install or update code.

Mitigation: Disable dependency auto-healing by default and review dependency changes before allowing them in shared or production workspaces.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/samwlh/skills/capability-evolver-bak)
- [EvoMap documentation](https://evomap.ai/wiki)
- [EvoMap platform](https://evomap.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown and text prompts with JSON evolution assets, inline shell commands, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write GEP assets, memory records, and source changes during solidification; review mode is available for human approval before changes are applied.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

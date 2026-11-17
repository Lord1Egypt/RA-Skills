## Description:

A self-evolution engine for AI agents. Analyzes runtime history to identify improvements and applies protocol-constrained evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuzimaki](https://clawhub.ai/user/wuzimaki)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent teams use this skill to inspect runtime history, identify failures or inefficiencies, and generate GEP-guided evolution prompts, assets, and reviewable repair guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read agent history and participate in autonomous evolution workflows.

Mitigation: Install it only in workspaces where log review and autonomous edits are acceptable, and use --review for sensitive projects.

Risk: The skill may contact an external hub or share evolution assets when collaboration paths are enabled.

Mitigation: Set EVOLVE_BRIDGE=false, avoid A2A_HUB_URL unless the hub is trusted, and set EVOLVER_AUTO_PUBLISH=false when sharing is not intended.

Risk: Auto-update or unreviewed command configuration can change behavior unexpectedly.

Mitigation: Set evolver.autoUpdate=false and do not set INTEGRATION_STATUS_CMD to unreviewed shell text.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wuzimaki/skills/evolver-repo)
- [EvoMap Documentation](https://evomap.ai/wiki)
- [EvoMap](https://evomap.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, and shell-command guidance generated as a single agent output stream]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local GEP assets and evolution artifacts when run in an enabled workspace.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

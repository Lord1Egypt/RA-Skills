## Description:

A self-evolution engine for AI agents. Analyzes runtime history to identify improvements and applies protocol-constrained evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent teams use this skill to analyze agent runtime history, identify recurring failures or inefficiencies, and generate protocol-constrained evolution guidance and assets for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad autonomous code, network, update, and reporting authority can affect a workspace beyond simple prompt generation.

Mitigation: Install and run it in a dedicated, backed-up test workspace before use in sensitive repositories.

Risk: Automatic execution, Hub publishing, GitHub issue reporting, and auto-update may create changes or external reports unexpectedly.

Mitigation: Disable those behaviors unless explicitly needed, and avoid running with ambient GitHub credentials.

Risk: Risky defaults can modify code or roll back workspace changes in ways users may not expect.

Mitigation: Use review mode and a non-destructive rollback setting before allowing the skill to apply or solidify changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lean-zhouchao/skills/capability-evolver-zc)
- [EvoMap Documentation](https://evomap.ai/wiki)
- [EvoMap Platform](https://evomap.ai)
- [Artifact README](README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prompts, JSON evolution assets, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local evolution artifacts and validation reports when run in a workspace.]

## Skill Version(s):

1.27.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

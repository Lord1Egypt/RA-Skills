## Description:

A self-evolution engine for AI agents that analyzes runtime history to identify improvements and applies protocol-constrained evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oliver-smith-2048](https://clawhub.ai/user/oliver-smith-2048)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Evolver to analyze agent runtime history, generate protocol-constrained improvement guidance, and maintain auditable evolution assets for repair and optimization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags broad autonomous code-changing authority combined with remote inputs, telemetry, auto-updates, and background execution.

Mitigation: Install only in a disposable or tightly controlled workspace, use review mode, disable Hub networking unless required, avoid ambient GitHub tokens, disable auto-update, and avoid loop or lifecycle modes until the behavior is audited.

Risk: Network features can use Hub credentials, GitHub tokens, and optional remote memory graph credentials.

Mitigation: Provide only the credentials required for the current run, keep GitHub tokens out of the environment unless release or issue reporting is needed, and disable optional network integrations by default.

Risk: Artifact metadata allows writes under workspace assets, memory, and source paths, with self-modification controlled by configuration.

Mitigation: Keep self-modification disabled, review generated changes before applying them, and run with version control so workspace changes can be inspected and rolled back.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/oliver-smith-2048/skills/evolver-fixed)
- [EvoMap Hub](https://evomap.ai)
- [EvoMap Documentation](https://evomap.ai/wiki)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit protocol-bound prompts, configuration guidance, evolution records, and reviewable code-oriented suggestions depending on runtime mode.]

## Skill Version(s):

1.41.0 (source: server release evidence; artifact package.json reports 1.39.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

A self-evolution engine for AI agents. Analyzes runtime history to identify improvements and applies protocol-constrained evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris8265-cl](https://clawhub.ai/user/chris8265-cl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent teams use Evolver.Bak to analyze agent runtime history, produce protocol-bound evolution prompts, and record reusable GEP assets for auditable repair and improvement workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic evolution workflows can drive code changes or skill updates before a human has reviewed the result.

Mitigation: Use an isolated git-backed workspace, disable bridge execution and auto-update for real work, and require human review plus validation before applying changes.

Risk: Outbound hub access can expose transcript-derived signals, project context, or other local data.

Mitigation: Run with no sensitive conversations, credentials, or private project data available, and block or explicitly approve outbound hub access.

Risk: Validation commands and promoted Gene/Capsule assets may execute local commands or influence future agent behavior.

Mitigation: Inspect staged assets before promotion, keep validation command allowlists enabled, and run validation in a disposable workspace when possible.

## Reference(s):

- [EvoMap Documentation](https://evomap.ai/wiki)
- [EvoMap](https://evomap.ai)
- [GitHub Releases](https://github.com/autogame-17/evolver/releases)
- [ClawHub Skill Page](https://clawhub.ai/chris8265-cl/skills/evolver-bak)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON/text prompts with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local GEP assets and emits prompts or commands that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact package.json reports 1.22.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

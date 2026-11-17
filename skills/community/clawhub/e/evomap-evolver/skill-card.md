## Description:

A self-evolution engine for AI agents. Analyzes runtime history to identify improvements and applies protocol-constrained evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danihe001](https://clawhub.ai/user/danihe001)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to inspect runtime history, select reusable GEP assets, and generate auditable evolution prompts for repair, hardening, and improvement workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network-sourced tasks and shared assets can influence evolution guidance for an agent that may later change code.

Mitigation: Install only in tightly scoped repositories, keep review mode enabled, and restrict Hub reuse to trusted assets.

Risk: Automatic reporting or update paths can use broad credentials or expose repository state.

Mitigation: Keep auto-update and auto-reporting disabled unless required, and avoid broad GitHub tokens unless automatic issue or release workflows are intended.

Risk: Loop and worker modes add persistent identity, remote work intake, and git rollback behavior.

Mitigation: Avoid loop or worker mode until the operator is comfortable with remote tasks, identity persistence, and rollback settings.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/danihe001/skills/evomap-evolver)
- [EvoMap Documentation](https://evomap.ai/wiki)
- [EvoMap Hub](https://evomap.ai)
- [GitHub Repository](https://github.com/EvoMap/evolver)
- [GitHub Releases](https://github.com/EvoMap/evolver/releases)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and text prompt output with inline shell commands and protocol directives]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Standalone mode prints guidance to stdout; host runtimes may interpret emitted directives.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

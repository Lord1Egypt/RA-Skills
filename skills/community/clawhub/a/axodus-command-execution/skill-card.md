## Description:

Execute terminal commands safely with preflight checks and risk gating.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzfshark](https://clawhub.ai/user/mzfshark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run repository inspections, tests, builds, migrations, and other terminal commands with preflight risk classification, confirmation gates, captured outputs, and follow-up diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Malformed trigger metadata could cause the skill to activate differently than intended.

Mitigation: Review and correct trigger metadata before publishing or installing the skill.

Risk: Broad command-running capability can affect files, network resources, or system state.

Mitigation: Keep confirmations enabled for destructive, installer, network, and system-level commands; prefer dry-run and scoped commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mzfshark/skills/axodus-command-execution)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [YAML-style structured command result with highlights and next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command purpose, result status, exit code, key output lines, and diagnostic next steps.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill.yml, and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

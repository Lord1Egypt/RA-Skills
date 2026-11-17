## Description:

Routes Cargo CLI tasks to the right Cargo skill and explains the shared setup, execution, and troubleshooting conventions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this entry point to choose the right Cargo skill, set up the CLI, and follow shared conventions for runs, batches, polling, and common failure modes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports unpinned install and update paths.

Mitigation: Review the installer and update path, and confirm the package version before installing or updating.

Risk: Diagnostic reports may disclose sensitive information.

Mitigation: Review diagnostic report contents and obtain approval before submission.

Risk: Run, batch, account, or workflow actions may go beyond the skill's routing purpose.

Mitigation: Inspect the proposed action and its scope, and require approval before running it.

## Reference(s):

- [Cargo prerequisites](references/prerequisites.md)
- [Cargo use cases](references/use-cases.md)
- [Interaction conventions](references/interaction.md)
- [Common gotchas](references/gotchas.md)
- [Glossary](references/glossary.md)
- [UUID flow](references/uuid-flow.md)
- [Cargo skills homepage](https://github.com/getcargohq/cargo-skills)
- [Cargo ClawHub skill page](https://clawhub.ai/cargo-ai/skills/cargo)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.37.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

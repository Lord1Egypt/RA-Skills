## Description:

Refactors research code into publication-ready, reproducible workflows by adding documentation, error handling, environment specifications, and validation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to refactor research analysis code for publication, collaboration, and reproducible execution. It helps analyze existing scripts, add documentation and error handling, define environments, and validate that results remain reproducible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged requirements include an unjustified `src` entry and unpinned dependencies.

Mitigation: Remove `src` and pin real dependency versions before installing the requirements in a clean environment.

Risk: Generated reproducibility metadata may include local machine details such as hostname and package inventory.

Mitigation: Review generated `reproducibility_info.json` before sharing or publishing outputs.

Risk: The generator writes refactored project files to an output directory.

Mitigation: Run it only against an intended project directory and choose a new empty output directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/code-refactor-for-reproducibility-1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with code snippets, shell commands, and generated project-file guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should separate assumptions, deliverables, risks, validation needs, and unresolved items.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

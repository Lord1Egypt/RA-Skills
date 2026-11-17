## Description:

This skill helps agents generate, run, diagnose, and iteratively correct CMG GEM reservoir or core-scale DAT simulation files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nv4dll-git](https://clawhub.ai/user/nv4dll-git)

### License/Terms of Use:

MIT-0

## Use Case:

Reservoir engineers and simulation specialists use this skill to draft CMG GEM DAT files, distinguish reservoir-scale and core-scale modeling patterns, run local simulator commands, and use output logs to correct model errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create or overwrite DAT files in a local project directory.

Mitigation: Use a dedicated project directory, choose filenames explicitly, and review changes before replacing existing work.

Risk: Local CMG GEM simulator runs may consume compute resources or licensed software capacity.

Mitigation: Confirm simulator execution before running commands and monitor local resource and license usage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nv4dll-git/skills/cmg-gem)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown text with DAT code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write DAT files and propose local CMG GEM simulator runs when explicitly requested.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

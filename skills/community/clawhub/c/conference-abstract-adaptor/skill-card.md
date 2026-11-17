## Description:

Adapt abstracts to meet specific conference word limits and formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, authors, and agents assisting with conference submissions use this skill to adapt abstract text for conference-specific word or character limits and expected section formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script reads local abstract files and can write adapted output to a user-selected path.

Mitigation: Use non-sensitive input files and direct outputs to a workspace or temporary directory.

Risk: The output path is not protected against overwriting important files or path traversal.

Mitigation: Review the --output path before execution and avoid existing or sensitive file locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/conference-abstract-adaptor)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Guidance]

**Output Format:** [Plain text abstract output with count verification and optional file output; Markdown usage guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports ASGCT, ASCO, SfN, AACR, and ASM conference presets.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

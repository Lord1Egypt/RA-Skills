## Description:

Generate random test data including text, numbers, UUIDs, and structured formats. Use when creating mock datasets, sample records, or randomized test inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use Generate to create mock datasets, sample records, and randomized test inputs for development and testing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI writes generation history to ~/.generate/data.jsonl, which may retain generated schemas or sample values.

Mitigation: Review or delete ~/.generate/data.jsonl periodically, and avoid generating sensitive sample data on shared machines.

Risk: CSV generation can create or overwrite files at a user-specified output path.

Mitigation: Run commands from an intended workspace and choose explicit output filenames to avoid overwriting existing files.

Risk: The password command emits random strings that are not suitable for real accounts or production secrets.

Mitigation: Use a dedicated cryptographic password generator for real credentials and limit this command to mock data.

## Reference(s):

- [Generate on ClawHub](https://clawhub.ai/bytesagain3/skills/generate)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, JSON, CSV, Shell commands, Configuration]

**Output Format:** [Plain text, JSON objects, CSV output or files, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generation history to ~/.generate/data.jsonl; CSV output can be written to a user-specified path.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

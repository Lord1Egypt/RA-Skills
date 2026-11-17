## Description:

Converts CSV files to JSON arrays with automatic type detection, custom delimiters, and optional compact or formatted output using only the Python standard library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and automation agents use this skill to convert CSV exports into JSON arrays for application import, database loading, or data analysis preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An existing file can be overwritten when the user chooses an output path with the -o option.

Mitigation: Confirm the destination path before running the converter and write to a new filename or backed-up location when preserving prior output matters.

Risk: The skill interface and messages are in Chinese, which may cause misuse by operators who cannot read the prompts or documentation.

Mitigation: Use the skill with Chinese-reading operators or translate the commands and messages before deployment.

Risk: The packaged documentation includes an unrelated promotional link.

Mitigation: Treat the promotional link as unrelated to CSV conversion and do not follow or rely on it when evaluating or operating the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-csv-to-json)
- [Packaged skill documentation](artifact/SKILL.md)
- [CSV conversion script](artifact/scripts/csv_to_json.py)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, JSON]

**Output Format:** [Markdown guidance with bash commands; the converter emits a JSON array to stdout or to a selected output file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a user-provided CSV path, supports a custom delimiter and compact output flag, and may overwrite an existing output file when -o points to that path.]

## Skill Version(s):

1.0.1 (source: server release metadata; packaged artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

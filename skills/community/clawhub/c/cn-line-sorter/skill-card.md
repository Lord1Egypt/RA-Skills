## Description:

Sorts, deduplicates, reverses, shuffles, and length-sorts lines in local text files using a Python standard-library helper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content operators, and other users can use this skill to clean and reorder local text lists such as keywords, to-dos, names, or sampling lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using -o or --output can overwrite an existing file at the selected output path.

Mitigation: Choose a new or disposable output filename, or back up any existing file before running the helper.

Risk: The helper reads user-selected local text files.

Mitigation: Run it only on files intended for local processing and review results before sharing generated output.

Risk: The skill documentation and command examples are in Chinese.

Mitigation: Install and use it only if the operator can understand or review the Chinese-language instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-line-sorter)
- [Publisher profile](https://clawhub.ai/user/freedompixels)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands]

**Output Format:** [Markdown with inline shell commands and plain-text file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-selected text files; using --output writes a file at the chosen path.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

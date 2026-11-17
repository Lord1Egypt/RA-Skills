## Description:

Detect text file encoding (UTF-8, GBK, Latin-1, etc), auto-detect BOM markers, and run with the Python standard library without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content or tooling operators use this skill to identify likely text-file encodings, especially for Chinese-language files, before processing, repair, or conversion workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The detector may misreport unsupported encodings or ambiguous files.

Mitigation: Treat results as a lightweight local check and verify uncertain detections before conversion or automated processing.

Risk: Very large files may expose robustness issues in file-size handling.

Mitigation: Avoid very large inputs until size handling is hardened, or run the tool in a controlled local environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-text-encoding-detector)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [JSON object printed to stdout, with brief agent guidance when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local file bytes; no network access or external dependencies are required.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

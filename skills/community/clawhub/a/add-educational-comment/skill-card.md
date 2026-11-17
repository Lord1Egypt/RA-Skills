## Description:

Add educational comments to the file specified, or prompt asking for file to comment if one is not provided.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhauga](https://clawhub.ai/user/jhauga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and learners use this skill to turn selected code files into learning resources by adding educational comments matched to configurable knowledge level, detail, and repetition settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Educational comments can unintentionally change behavior or break syntax in whitespace-sensitive or encoding-sensitive files.

Mitigation: Review diffs before accepting changes and validate formatting, encoding, indentation, and syntax after the skill edits a file.

Risk: Added explanations may be inaccurate, excessive, or mismatched to the learner's level.

Mitigation: Use the configuration options for detail, repetitiveness, user knowledge, and educational level, then review the generated comments for accuracy.

## Reference(s):

- [PEP 263 - Defining Python Source Code Encodings](https://peps.python.org/pep-0263/)
- [ClawHub skill page](https://clawhub.ai/jhauga/skills/add-educational-comment)
- [Publisher profile](https://clawhub.ai/user/jhauga)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance and edited code-file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May add educational comments to user-selected files while preserving encoding, line endings, indentation, and build correctness.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

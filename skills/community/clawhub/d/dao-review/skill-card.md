## Description:

DaoReview reviews .docx, .txt, and .md documents in Chinese and scores them across structure, content quality, formatting, logic, and actionability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[douglasliu](https://clawhub.ai/user/douglasliu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use DaoReview to ask an agent to inspect uploaded or local documents and return an objective Chinese review report with scores, strengths, problems, and improvement suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses shell command templates to read document paths, which could execute unintended commands if an untrusted path is crafted maliciously.

Mitigation: Use trusted filenames and documents, and prefer safe file-reading APIs or argument-array execution before handling untrusted uploads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/douglasliu/skills/dao-review)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese Markdown document review report with a score, strengths, issues, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports .docx, .txt, and .md inputs; replies in Chinese.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

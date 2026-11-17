## Description:

Compress academic abstracts to meet strict word limits while preserving key information, scientific accuracy, and readability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, authors, and academic support teams use this skill to shorten English academic abstracts for journal submissions, conference applications, and grant proposals while preserving important scientific content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script reads input text from a provided path or stdin, which can expose sensitive abstracts or draft content to the local agent workflow.

Mitigation: Use only abstracts or text files intended for processing, keep inputs inside the current workspace, and avoid sensitive or confidential documents.

Risk: The --output option writes to the supplied path and can overwrite any file the agent process is allowed to modify.

Mitigation: Write to a new or disposable output path and review the destination before running the command.

Risk: Automated compression can remove context or alter the emphasis of scientific claims.

Mitigation: Have a qualified human review the trimmed abstract for scientific accuracy, quantitative integrity, and readability before submission.

## Reference(s):

- [Abstract Trimmer on ClawHub](https://clawhub.ai/aipoch-ai/skills/abstract-trimmer)
- [aipoch-ai Publisher Profile](https://clawhub.ai/user/aipoch-ai)
- [Abstract Trimmer References](references/guidelines.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands]

**Output Format:** [JSON or plain text trimmed abstract output, with optional file output when an output path is provided.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes original word count, final word count, and reduction percentage in JSON mode.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

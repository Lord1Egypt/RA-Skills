## Description:

Doc Beautifier helps agents reformat Word .docx documents by detecting titles, headings, and body text, then applying consistent fonts, spacing, margins, page numbers, and one of three template styles while preserving original text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangchao0106](https://clawhub.ai/user/tangchao0106)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they want an agent to clean up the presentation of an existing .docx document while preserving its text. The skill guides the agent to run the bundled formatter, choose a built-in template style, validate the result, and return the output document path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The formatter may replace existing visual styling with opinionated fonts, A4 page settings, margins, and centered page numbers.

Mitigation: Run it on a copy of the document and review the output before replacing the original.

Risk: Heuristic structure detection may misclassify titles, headings, or body paragraphs.

Mitigation: Inspect the formatted document and adjust the source styles or template settings before sharing the result.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown with inline shell commands and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a formatted .docx file at the requested output path when the bundled script is run.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

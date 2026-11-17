## Description:

This skill helps agents handle common PDF tasks, including text and table extraction, PDF creation, merge and split operations, watermarking, password protection, and OCR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill for explicit PDF processing tasks such as extracting text or tables, creating PDFs, merging or splitting files, adding watermarks, password-protecting documents, and running OCR.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill broadens into generic command, network, API, and file-processing behavior beyond its stated PDF purpose.

Mitigation: Use it only for explicit PDF tasks and review any proposed generic shell, network, or API action before execution.

Risk: PDF generation, merge, split, or conversion workflows can overwrite important documents if output locations are ambiguous.

Mitigation: Specify output paths and filenames before allowing write operations.

Risk: The security verdict is suspicious even though no specific risk findings were listed.

Mitigation: Review the skill before installation and keep command execution constrained to approved PDF tooling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/document-pdf-tool-free)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks, command suggestions, configuration snippets, and generated or transformed PDF-related files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce structured operation status, extracted text or tables, and output files when the agent has appropriate file and command tools.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Reads and summarizes cognitive neuroscience and experimental psychology papers from PDFs or plain text, extracting structured notes on hypotheses, methods, participants, tasks, statistics, effect sizes, results, and limitations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guigui855](https://clawhub.ai/user/guigui855)

### License/Terms of Use:

MIT-0

## Use Case:

External users, students, researchers, and reviewers use this skill to turn cognitive neuroscience or experimental psychology papers into structured, critical-reading summaries with domain terms and statistics called out.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Summaries may omit, misstate, or overinterpret paper details, especially statistics and limitations.

Mitigation: Review the generated summary against the original paper and verify reported statistics, effect sizes, uncertainty, and limitations before relying on it.

Risk: Scanned or poorly extracted PDFs can leave the agent without reliable paper text.

Mitigation: If text extraction returns no usable content, ask for OCR or extracted text and avoid fabricating missing content.

## Reference(s):

- [Domain Glossary - Attention, Memory, & Population Neuroscience](references/domain-glossary.md)
- [Statistics Guide - Reading the Numbers in These Papers](references/statistics-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/guigui855/skills/cogneuro-paper-reader)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown structured summary with optional inline shell command guidance for PDF text extraction]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes citation, plain-language summary, methods, analyses, key results, limitations, key terms, and critical-reading notes; unavailable source details should be reported as not reported.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

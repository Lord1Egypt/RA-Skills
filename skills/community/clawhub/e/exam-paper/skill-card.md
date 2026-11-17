## Description:

Exam Paper helps agents generate exam-paper and answer-key PDFs from question-bank JSON, manage question banks, and track wrong-answer review records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kreator666](https://clawhub.ai/user/kreator666)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, tutors, students, and agents use this skill to assemble practice exams, export printable papers with answer keys, maintain subject question banks, and record wrong answers for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted question-bank or exam JSON can escape intended file boundaries or affect PDF generation.

Mitigation: Use only trusted JSON inputs, validate subject names and output paths, and run the skill in a constrained workspace.

Risk: PDF generation depends on reportlab and local font handling.

Mitigation: Install a pinned reportlab version in a virtual environment and verify generated PDFs before distributing them.

## Reference(s):

- [Exam Formats](references/exam-formats.md)
- [Informatics Topics](references/informatics.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON formats, and generated PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces exam and answer-key PDFs through local Python scripts; question and error data are stored as JSON files.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

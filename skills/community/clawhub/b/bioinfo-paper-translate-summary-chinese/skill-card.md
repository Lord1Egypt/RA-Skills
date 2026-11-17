## Description:

Translates English research-paper PDFs into Chinese and organizes the result for bioinformatics-focused reading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zd200572](https://clawhub.ai/user/zd200572)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and agents working with bioinformatics papers use this skill to extract text from a trusted English PDF, translate it into Chinese, and produce a Markdown summary emphasizing bioinformatics details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF text, including sensitive or proprietary paper contents, is exposed directly to the agent context.

Mitigation: Use only trusted PDFs whose contents may be shared with the agent, and avoid sensitive or proprietary papers unless that exposure is acceptable.

Risk: The artifact writes a predictable temporary text file in the same directory as the PDF.

Mitigation: Run the skill in a private working directory with trusted files, normal user privileges, and no shared writable directory.

Risk: PDF conversion quality may be limited for scanned or complex PDFs.

Mitigation: Install poppler-utils and review the extracted text and final summary before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zd200572/skills/bioinfo-paper-translate-summary-chinese)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text containing extracted PDF text and instructions for a Chinese Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pdftotext from poppler-utils and an absolute PDF path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Develop deposition question sets from Relativity-exported PDF productions using a user-provided legal theory, including page-level document ID extraction, relevance mapping, rationales, and supporting quotes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chipmunkrpa](https://clawhub.ai/user/chipmunkrpa)

### License/Terms of Use:

MIT-0

## Use Case:

External legal practitioners and litigation-support teams use this skill to analyze Relativity-exported PDF productions against a case theory and draft deposition questions grouped by document ID. It supports question drafting with reasons, verbatim supporting quotes, and source file/page references for follow-up if testimony is denied.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated JSON and final question sets may contain sensitive legal document text from user-provided PDFs.

Mitigation: Run the extraction only against intended case PDFs and treat generated JSON and Markdown outputs as sensitive case materials.

Risk: The extraction workflow depends on an unpinned pdfplumber installation.

Mitigation: Install in a project virtual environment where possible and pin or review pdfplumber before use.

Risk: Document IDs and quotes extracted from PDFs may require legal or factual verification before use in deposition preparation.

Mitigation: Review pages with missing document IDs and manually verify selected quotes, page references, and question relevance before relying on the output.

## Reference(s):

- [Deposition Output Template](references/deposition_output_template.md)
- [Deposition Question Development on ClawHub](https://clawhub.ai/chipmunkrpa/skills/deposition-question-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown deposition question sets with optional shell commands and JSON extraction output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Questions are grouped by document ID and include a reason, supporting quote, and source file/page reference.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

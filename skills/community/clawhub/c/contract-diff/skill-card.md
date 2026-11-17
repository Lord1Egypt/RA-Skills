## Description:

Compare contract templates with scanned stamped contracts, list all differences including additions, deletions, and modifications, and output a Word document for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[russell-yu](https://clawhub.ai/user/russell-yu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and review teams use this skill to compare a contract template with a scanned signed contract and identify changed, added, or removed terms. It is suited for document review support, with human review required for key clauses because OCR can be inaccurate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive legal documents and may print detailed contract text to logs.

Mitigation: Run it only in an isolated environment, avoid unnecessary logging, and remove sensitive source documents and generated reports after review.

Risk: The helper script can silently install unpinned Python packages at runtime.

Mitigation: Install reviewed, pinned dependencies yourself before use and avoid runtime dependency installation in managed or legal-document environments.

Risk: OCR-based extraction and highlighting can miss or misplace important contract changes.

Mitigation: Treat generated differences and highlights as review aids and have a qualified reviewer verify key clauses against the original documents.

## Reference(s):


## Skill Output:

**Output Type(s):** [analysis, markdown, code, shell commands, files]

**Output Format:** [Word document or Markdown report with categorized differences, similarity scores, and optional highlighted image output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce report.docx, Markdown reports, highlighted.png, and console summaries; OCR-based results should be manually checked for important legal terms.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

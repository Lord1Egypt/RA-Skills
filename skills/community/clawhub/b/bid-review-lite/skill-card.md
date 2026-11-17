## Description:

AI-powered bid/tender document review. Extracts text from .docx/.doc files, cross-references bid requirements vs responses, and generates a detailed audit report with risk ratings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zacjiang](https://clawhub.ai/user/zacjiang)

### License/Terms of Use:


## Use Case:

Bid managers, procurement officers, and quality reviewers use this skill to compare procurement requirements against bid responses and identify pricing, eligibility, technical, integrity, and compliance issues before making or finalizing bid decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned Python dependencies may vary across environments.

Mitigation: Install dependencies in a virtual environment and prefer pinned versions when operationalizing the skill.

Risk: The generated bid review may miss issues in images, seals, certificates, or other visual evidence because the lite artifact is text-based.

Mitigation: Use the report as an aid for human procurement review and manually inspect visual or scanned evidence before making compliance decisions.

Risk: Legacy .doc extraction may be incomplete or lossy.

Mitigation: Check extracted text against the original document, especially for critical pricing, eligibility, and certification details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zacjiang/skills/bid-review-lite)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, guidance]

**Output Format:** [Markdown report with checklist tables, issue sections, risk ratings, and optional extracted text files from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report is intended to support human procurement review and should not be treated as a final compliance decision.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Audits Chinese business documents with deterministic rules and returns traceable findings and reports in HTML, JSON, or Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nohn3043-arch](https://clawhub.ai/user/nohn3043-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, compliance reviewers, and document owners use the engine to review Chinese contracts, regulations, official documents, and other business documents locally, then inspect reproducible findings and suggested fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted document can insert unwanted browser scripts into an HTML report.

Mitigation: Use JSON output until HTML generation safely escapes document and rule content; avoid opening or sharing HTML reports from untrusted documents.

Risk: The demo can overwrite report files with matching names in its output directory.

Mitigation: Run demos in a new, empty directory.

Risk: Custom rules can affect audit findings.

Mitigation: Use trusted custom rules and keep document sizes manageable.

## Reference(s):

- [Usage Guide](artifact/references/UsageGuide.md)
- [Rule Catalog](artifact/references/RuleCatalog.md)
- [Project homepage](https://github.com/nohn3043-arch/Story-engine)

## Skill Output:

**Output Type(s):** [JSON, Markdown, HTML]

**Output Format:** [Single-file audit reports with findings and an audit trace]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic rule-based findings include severity, matched text, location, and suggested fixes.]

## Skill Version(s):

1.1.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Collects e-commerce category URLs, extracts category hierarchy data, and saves structured results as CSV files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qirongzhang](https://clawhub.ai/user/qirongzhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to turn e-commerce collection URLs into CSV rows containing the original URL, category path, domain, and parsed category levels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes CSV files to the local filesystem, and the bundled default output path is user-specific.

Mitigation: Set an explicit output directory appropriate for the runtime before using the collector.

Risk: CSV rows built from links supplied by other people may contain values that spreadsheet applications treat as formulas.

Mitigation: Treat generated CSVs as untrusted and sanitize or review formula-like cells before opening them in spreadsheet software.

Risk: Included tests may create and remove paths under /tmp.

Mitigation: Review the test cleanup path before running tests on shared systems.

## Reference(s):

- [Skill README](README.md)
- [Usage Examples](examples/usage.md)
- [ClawHub Skill Page](https://clawhub.ai/qirongzhang/skills/category-link-collector)
- [Publisher Profile](https://clawhub.ai/user/qirongzhang)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, files]

**Output Format:** [CSV files and Markdown or shell guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CSV output uses URL-derived category fields and may write to a configurable local output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

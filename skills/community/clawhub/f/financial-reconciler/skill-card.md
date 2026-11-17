## Description:

Privacy-first personal finance tracker with local SQLite storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gowtham1984](https://clawhub.ai/user/gowtham1984)

### License/Terms of Use:


## Use Case:

External users use this skill to import local bank statement files, categorize transactions, track budgets, ask spending questions, and generate finance reports while keeping data on their own machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Imported bank transactions are stored in a local SQLite database.

Mitigation: Install only if local storage of personal finance data is acceptable, and protect the configured data directory with normal device and filesystem controls.

Risk: HTML reports may turn imported transaction text into active browser content.

Mitigation: Prefer text or JSON reports, and avoid opening HTML reports generated from untrusted or modified statement data until HTML escaping is fixed.

Risk: The skill installs and runs local Python dependencies and scripts.

Mitigation: Use a virtual environment and import statements only from trusted sources.

## Reference(s):

- [Category Guide](references/category_guide.md)
- [Query Examples](references/query_examples.md)
- [Supported Bank Formats](references/supported_banks.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Conversational Markdown with inline shell commands and parsed JSON, text, or HTML report summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying scripts emit JSON for imports, categorization, queries, budgets, and reports; reports may also be generated as text or HTML.]

## Skill Version(s):

1.0.0 (source: skill.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

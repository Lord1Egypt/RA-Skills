## Description:

This skill helps legal professionals and general users search Chinese court judgment cases, retrieve similar cases, filter by case reason, court, document type, and date, and summarize retrieved case information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolalam](https://clawhub.ai/user/coolalam)

### License/Terms of Use:

MIT-0

## Use Case:

External users, legal professionals, and agent operators use this skill to search public Chinese court judgment documents, compare similar cases, and produce concise case lists, case details, and judicial-rule summaries. It is a retrieval and presentation aid, not a source of legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The case-search script sends API credentials and legal search text, including long-form case materials, to an external Deli Legal API while TLS verification is disabled.

Mitigation: Review the skill before using it with real case materials, redact confidential or personal information from inputs, and do not use sensitive API keys unless TLS verification is fixed.

Risk: Retrieved court-document coverage may be incomplete because public judgment availability depends on court publication practices and legal restrictions.

Mitigation: Treat results as retrieval support only, cite complete case identifiers when using them, and verify important cases against official court documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coolalam/skills/case-retrieval)
- [Search examples](references/search-examples.md)
- [Deli Legal case search API endpoint](https://platform.delilegal.com/api/v1/generice/case/list)
- [Deli Legal API key console](https://open.delilegal.com/personal/keys)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown case listings, tables, summaries, and command or configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include retrieved case metadata, case details, similar-case comparisons, judicial-rule summaries, pagination guidance, and no-result guidance.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

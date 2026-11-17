## Description:

Run explicit Extruct API tasks through the bundled Extruct CLI. Covers Deep Search, semantic search, lookalike search, company and people tables, column operations, enrichment, and contact finding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zkid18](https://clawhub.ai/user/zkid18)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to operate Extruct company discovery, Deep Search, AI Tables, enrichment, scoring, and contact-finding workflows through guided CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated Extruct operations can mutate tables, rows, columns, or run bulk work.

Mitigation: Inspect the target table, rows, and columns before changes, and require explicit confirmation before deletes or bulk runs.

Risk: People and contact enrichment can involve email, phone, or LinkedIn data.

Mitigation: Use contact enrichment only where the user has authorization and a lawful business basis.

Risk: Documented command behavior may differ from the live Extruct API.

Mitigation: Consult the official Extruct API reference when request shape, fields, response contracts, or endpoint capabilities are uncertain.

## Reference(s):

- [Extruct API Reference](https://www.extruct.ai/docs/api-reference/introduction)
- [Column Guide](references/column-guide.md)
- [Finding Companies](references/finding-companies.md)
- [Researching Companies](references/researching-companies.md)
- [Finding People At Companies](references/finding-people-at-companies.md)
- [Researching People](references/researching-people.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Extruct CLI commands and operational summaries; authenticated actions depend on the user's Extruct account.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

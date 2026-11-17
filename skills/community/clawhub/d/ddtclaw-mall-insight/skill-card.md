## Description:

Searches published mall data by mall name to support mall research, leasing, brand expansion, and visit preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

Retail leasing, site-selection, and brand-expansion teams use the skill to research a named mall and prepare visits using published mall, tenant, competitor, neighborhood, event, and sentiment data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A DDT_API_KEY is required, and mall data queries consume account points; a timeout can leave charge status uncertain.

Mitigation: Provide the key through the environment variable and keep it out of chat and logs. Confirm the mall and radius before a full query, and check account usage before retrying.

Risk: The security assessment is partial because a referenced output file was unavailable to the scanners.

Mitigation: Review that file if it is included before relying on the clean verdict.

## Reference(s):

- [店店通 homepage](https://gotoshop-ai.com/ddtclaw/)
- [Mall data contract](artifact/references/data-contract.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Chinese-language summaries and tables in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Grounded in the retrieved published data; distinguishes data facts from recommendations and reports missing coverage where relevant.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

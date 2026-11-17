## Description:

AMiner Free Search helps agents use AMiner free-tier APIs for lightweight academic paper, scholar, institution, venue, and patent lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canxiangcc](https://clawhub.ai/user/canxiangcc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to run low-cost academic discovery workflows, including paper triage, scholar identification, institution and venue normalization, patent trend scans, and deciding whether a paid AMiner API path is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad academic activation may route ordinary academic queries to AMiner without clear user intent.

Mitigation: Confirm that the user wants AMiner free-tier lookup before sending query terms to the provider, especially for private, unpublished, or sensitive research topics.

Risk: The skill requires an AMiner API key and examples include token handling.

Mitigation: Store AMINER_API_KEY as an environment variable, verify only whether it exists, and avoid printing or pasting real tokens into chat.

## Reference(s):

- [AMiner Free Search API Catalog](references/api-catalog.md)
- [AMiner Console](https://open.aminer.cn/open/board?tab=control)
- [AMiner Open Platform Documentation](https://open.aminer.cn/open/docs)
- [ClawHub Skill Page](https://clawhub.ai/canxiangcc/skills/aminer-free-academic)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline curl commands and concise result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should stay within AMiner free-tier capabilities, include AMiner entity URLs when IDs are available, and clearly state when a paid API is required.]

## Skill Version(s):

1.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

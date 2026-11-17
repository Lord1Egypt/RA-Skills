## Description:

Automates literature retrieval from PubMed and Feishu Bitable management for creating or supplementing research paper databases with translated metadata, journal metrics, and formatted references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenruao](https://clawhub.ai/user/chenruao)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, clinicians, and knowledge-management teams use this skill to create or update Feishu literature databases from PubMed searches, including deduplication, metadata extraction, Chinese translations, journal metrics, and GB/T reference formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses high-impact Feishu permission management, including full_access grants.

Mitigation: Confirm any full_access permission grant before use and avoid enabling the Feishu permission-management tool globally unless that capability is required.

Risk: The skill reads existing Feishu table records to deduplicate PMIDs.

Mitigation: Use it only with Feishu tables intended for literature management and avoid exposing unrelated or sensitive records.

Risk: Persistent Feishu tool configuration can broaden future agent actions.

Mitigation: Review Feishu channel configuration before deployment and keep permission-management capability scoped to expected workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chenruao/skills/feishu-literature-manager)
- [Field Mapping Reference](references/field_mapping.md)
- [Impact Factors and Journal Partitions](references/impact_factors.md)
- [PubMed ESearch Endpoint](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi)
- [PubMed EFetch Endpoint](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, API Calls]

**Output Format:** [Markdown with inline code blocks and structured field mappings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to create or update Feishu Bitables, retrieve PubMed metadata, deduplicate PMIDs, translate titles and abstracts, and set table permissions when the required tools are enabled.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

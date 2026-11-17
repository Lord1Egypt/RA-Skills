## Description:

Discovers hidden competitors in deep-tech domains by tracing academic citation networks from a paper, professor, or company to related researchers, patents, company registrations, and commercialization signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianzhiceng297-boop](https://clawhub.ai/user/tianzhiceng297-boop)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to investigate university spin-offs, professor-founded companies, and other deep-tech markets where competitors may be visible first through papers, patents, and citation relationships.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research workflows may collect unnecessary personal details about researchers.

Mitigation: Use public, lawfully obtained sources and limit collection to details needed to assess technology, patent, company, funding, and commercialization relevance.

Risk: Company, patent, funding, or commercialization claims may be outdated, incomplete, or inaccurate.

Mitigation: Verify claims across authoritative public records, patent databases, company registries, funding announcements, and primary company or institution sources before relying on them.

Risk: Citation proximity can be mistaken for genuine market competition.

Mitigation: Apply the similarity filtering checklist before retaining candidates, including technology overlap, performance comparison, improvement claims, and independent research group checks.

## Reference(s):

- [Detailed Workflow](references/workflow.md)
- [Checklists and Scoring Rules](references/checklists.md)
- [Real Case: Spot-Size Converter](examples/real-case-spot-size-converter.md)
- [Semantic Scholar References API](https://api.semanticscholar.org/graph/v1/paper/{paper_id}/references)
- [Semantic Scholar Citations API](https://api.semanticscholar.org/graph/v1/paper/{paper_id}/citations)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown research report with tables, competitor profiles, citation graph summaries, timelines, positioning matrices, and follow-up recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should distinguish verified evidence from hypotheses and should cite public sources used during research.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and changelog list 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

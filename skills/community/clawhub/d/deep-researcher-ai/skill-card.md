## Description:

Generate comprehensive 30-40 page academic research papers with full citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roboticresults](https://clawhub.ai/user/roboticresults)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, students, analysts, and developers use this skill to plan, source, draft, and quality-check long-form academic research papers with citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated research may contain incorrect, unsupported, or stale claims despite the workflow's citation requirements.

Mitigation: Review cited sources and cross-check high-impact claims against primary sources before relying on or publishing output.

Risk: The included QA script has correctness issues and should not be treated as a reliable validator.

Mitigation: Use the QA script only as a supplemental check and perform manual citation, source, and factual review.

Risk: The skill may run substantial public web or API research and produce local paper, source, and QA report files.

Mitigation: Use it in an appropriate research workspace and avoid entering confidential topics or sources unless approved.

## Reference(s):

- [Deep Researcher workflow](artifact/research_workflow.md)
- [Data sources registry](artifact/data_sources.md)
- [Citation and reference guide](artifact/reference_management.md)
- [Quality assurance system](artifact/quality_assurance.md)
- [Research paper template](artifact/research_paper_template.md)
- [arXiv API](https://export.arxiv.org/api/query)
- [PubMed E-utilities](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/)
- [World Bank API](https://api.worldbank.org/v2/)
- [Semantic Scholar API](https://api.semanticscholar.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown research paper with citations, source notes, verification logs, and a QA report; optional PDF or DOCX through companion skills.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets 15,000-18,000 words, 40-80 sources, and APA 7th citations by default.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

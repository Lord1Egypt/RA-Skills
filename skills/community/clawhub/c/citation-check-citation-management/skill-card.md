## Description:

Comprehensive citation management for academic research. Search Google Scholar and PubMed for papers, extract accurate metadata, validate citations, and generate properly formatted BibTeX entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, writers, and developer agents use this skill to search scholarly sources, extract publication metadata, validate citation accuracy, and prepare clean BibTeX bibliographies for academic writing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Citation identifiers, search queries, and optional NCBI email or API key values may be sent to scholarly services.

Mitigation: Use non-sensitive queries and credentials, review service terms, and configure only the API credentials needed for the task.

Risk: The evidence flags Google Scholar proxy and IP-switching guidance as risky.

Mitigation: Do not enable free-proxy or rate-limit bypass behavior; prefer official APIs and normal rate limits.

Risk: The evidence says the skill references an absent schematic-generation command.

Mitigation: Do not run schematic-generation commands unless the referenced script or skill is separately installed and reviewed.

Risk: Bibliography formatting workflows can write over citation files.

Mitigation: Run in an isolated environment with pinned dependencies and write to a new output file or backup before replacing existing bibliographies.

## Reference(s):

- [Citation Management Skill Page](https://clawhub.ai/wu-uk/skills/citation-check-citation-management)
- [BibTeX Formatting Guide](references/bibtex_formatting.md)
- [Citation Validation Guide](references/citation_validation.md)
- [Google Scholar Search Guide](references/google_scholar_search.md)
- [Metadata Extraction Guide](references/metadata_extraction.md)
- [PubMed Search Guide](references/pubmed_search.md)
- [Citation Checklist](assets/citation_checklist.md)
- [Google Scholar](https://scholar.google.com/)
- [PubMed](https://pubmed.ncbi.nlm.nih.gov/)
- [CrossRef API](https://api.crossref.org/)
- [PubMed E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
- [arXiv API](https://arxiv.org/help/api/)
- [DataCite API](https://api.datacite.org/)
- [DOI Resolver](https://doi.org/)
- [MeSH Browser](https://meshb.nlm.nih.gov/search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, plus optional JSON, BibTeX, and validation report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call external scholarly services and may write bibliography or report files when the agent follows the documented workflows.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

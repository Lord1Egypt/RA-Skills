## Description: <br>
Academic Research Hub helps agents search academic papers, download available documents, extract citations, and gather scholarly metadata across arXiv, PubMed, and Semantic Scholar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anisafifi](https://clawhub.ai/user/anisafifi) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to run literature searches, collect paper metadata, download available PDFs, and export citations or bibliographies for academic workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs network searches and user-directed downloads from academic sources. <br>
Mitigation: Use a virtual environment, keep dependencies updated, and direct downloads and exports to a dedicated project folder. <br>
Risk: Generated results and downloaded papers may be incomplete, stale, unavailable, or subject to source access restrictions. <br>
Mitigation: Review metadata and source links before relying on results, and confirm licensing or access rights before redistributing downloaded content. <br>
Risk: The artifact mentions Google Scholar, but the security guidance says support should be treated as undocumented or unavailable unless the maintainer updates the implementation. <br>
Mitigation: Rely on arXiv, PubMed, and Semantic Scholar behavior unless updated implementation evidence documents Google Scholar support. <br>


## Reference(s): <br>
- [Academic Research Hub README](references/readme.md) <br>
- [arXiv category taxonomy](https://arxiv.org/category_taxonomy) <br>
- [arXiv API documentation](https://arxiv.org/help/api) <br>
- [NCBI Entrez Programming Utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and shell commands, with generated research results available as text, JSON, BibTeX, RIS, Markdown, or downloaded PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write user-directed result files and arXiv PDF downloads to local output paths.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

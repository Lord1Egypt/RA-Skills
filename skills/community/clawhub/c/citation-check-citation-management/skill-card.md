## Description: <br>
Citation Management helps agents search Google Scholar and PubMed, extract and validate citation metadata, and generate properly formatted BibTeX entries for academic writing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developers use this skill to find scholarly sources, verify citation metadata, convert identifiers such as DOI, PMID, and arXiv IDs into BibTeX, and clean bibliographies before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs network lookups against academic metadata and search services. <br>
Mitigation: Use it only with citations and identifiers that are appropriate to send to external services, and avoid confidential identifiers or internal URLs. <br>
Risk: Bibliography formatting and validation workflows may write or overwrite local files. <br>
Mitigation: Use explicit output paths and keep backups before running formatting, validation, or auto-fix commands. <br>
Risk: The artifact includes proxy or IP-switching guidance for Google Scholar access. <br>
Mitigation: Avoid proxy or IP-switching behavior and follow the applicable service terms and institutional policies. <br>
Risk: The artifact includes unrelated schematic-generation and promotional instructions. <br>
Mitigation: Ignore those instructions unless they are explicitly relevant to the user request. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wu-uk/citation-check-citation-management) <br>
- [Publisher profile](https://clawhub.ai/user/wu-uk) <br>
- [BibTeX Formatting](references/bibtex_formatting.md) <br>
- [Citation Validation](references/citation_validation.md) <br>
- [Google Scholar Search](references/google_scholar_search.md) <br>
- [Metadata Extraction](references/metadata_extraction.md) <br>
- [PubMed Search](references/pubmed_search.md) <br>
- [Citation Quality Checklist](assets/citation_checklist.md) <br>
- [CrossRef API](https://api.crossref.org/) <br>
- [PubMed E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/) <br>
- [arXiv API](https://arxiv.org/help/api/) <br>
- [DataCite API](https://api.datacite.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and BibTeX outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce bibliography files, validation reports, and metadata exports when scripts are run by an agent.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Searches biomedical literature, retrieves citation counts, and helps import selected references to Zotero or EndNote/RIS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Merdeng](https://clawhub.ai/user/Merdeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, clinicians, students, and developers use this skill to search for biomedical papers by DOI, title, author, keyword, or PMID, then prepare selected references for Zotero or EndNote workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Literature queries and identifiers are sent to PubMed/NCBI, OpenAlex, and Zotero. <br>
Mitigation: Use the skill only when sharing those queries and identifiers with the relevant external services is acceptable. <br>
Risk: Zotero import operations require an API key that can modify a Zotero library. <br>
Mitigation: Use a Zotero API key with the minimum permissions needed and rotate or revoke it if exposure is suspected. <br>
Risk: Batch imports or RIS generation can add or export unintended references if PMID or DOI lists are wrong. <br>
Mitigation: Review PMID and DOI lists before batch import, and choose RIS output paths intentionally. <br>


## Reference(s): <br>
- [Academic Paper Finder release page](https://clawhub.ai/Merdeng/academic-paper-finder) <br>
- [Zotero API key settings](https://www.zotero.org/settings/keys/new) <br>
- [PubMed](https://pubmed.ncbi.nlm.nih.gov/) <br>
- [Zotero API](https://api.zotero.org) <br>
- [OpenAlex API](https://api.openalex.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands; scripts may emit terminal text, JSON search results, Zotero API writes, or RIS files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Zotero credentials for Zotero import operations; RIS generation writes to the user-selected output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

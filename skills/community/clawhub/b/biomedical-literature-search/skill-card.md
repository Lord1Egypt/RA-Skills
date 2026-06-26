## Description: <br>
Search PubMed and bioRxiv for biomedical research papers with titles, abstracts, metadata, and links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hollyya](https://clawhub.ai/user/hollyya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, biomedical analysts, and drug discovery teams use this skill to search PubMed by keyword and fetch recent bioRxiv preprints by date or category for literature review and topic exploration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Biomedical search terms, dates, and category filters are sent to external PubMed/NCBI and bioRxiv APIs. <br>
Mitigation: Avoid confidential project names, unpublished research strategy, or sensitive medical details in queries unless external disclosure is acceptable. <br>
Risk: Returned literature metadata and abstracts may be incomplete, unavailable, or limited by source API behavior. <br>
Mitigation: Review source links and primary records before relying on results for biomedical research decisions. <br>


## Reference(s): <br>
- [PubMed E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25500/) <br>
- [bioRxiv API](https://api.biorxiv.org/) <br>
- [ClawHub skill page](https://clawhub.ai/hollyya/biomedical-literature-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and structured paper-result fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns paper metadata such as title, authors, abstract, DOI, publication date, source category, and source link.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

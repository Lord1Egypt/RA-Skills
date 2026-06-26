## Description: <br>
Full-stack academic research assistant for searching papers, extracting publication-ready BibTeX from PDF headers, parsing full TEI XML document structure through GROBID, archiving to Zotero, and serving local PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bigdogaaa](https://clawhub.ai/user/bigdogaaa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and academic developers use this skill to find papers, download PDFs, extract citation metadata or full-text structure, and archive results into Zotero-backed research libraries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDFs may be downloaded from arbitrary URLs and sent to the configured GROBID service for parsing. <br>
Mitigation: Use trusted PDF sources and configure a local or trusted private GROBID endpoint, especially for sensitive documents. <br>
Risk: The local PDF server can expose downloaded PDFs if bound to an untrusted network interface. <br>
Mitigation: Keep the PDF server bound to localhost or a trusted private network, and do not expose it directly to the public internet. <br>
Risk: Zotero archiving requires API credentials and can write to the configured library. <br>
Mitigation: Use a limited Zotero API key and verify the target library and collection before enabling archiving workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bigdogaaa/academic-talon) <br>
- [GROBID documentation](https://grobid.readthedocs.io/) <br>
- [Zotero API key settings](https://www.zotero.org/settings/keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [JSON action results, BibTeX text, TEI XML, local file paths, and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download PDFs, cache parsed XML locally, update Zotero libraries, and return local PDF links when configured.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

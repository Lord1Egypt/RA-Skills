## Description: <br>
Search NCBI GEO/SRA, NGDC-GSA, and CNGB for biomedical datasets by disease, treatment, species, pathology subtype, and data type. Returns bold dataset ID, links, and article info in a structured table. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gateswell](https://clawhub.ai/user/gateswell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, clinicians, and biomedical data analysts use this skill to find public biomedical datasets matching disease, treatment, species, pathology subtype, and assay-type criteria across NCBI, NGDC, and CNGB sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Biomedical dataset or article metadata could be misleading if an external source returns no results or incomplete records. <br>
Mitigation: Use only dataset IDs and article metadata returned by the queried APIs, leave unavailable fields blank, and report no matching public datasets when searches return no results. <br>
Risk: CNGB searches may require an optional access token for controlled-access data. <br>
Mitigation: Ask before using a token, pass it only for the CNGB request, and do not hardcode or log the token. <br>
Risk: Search terms are sent to public biomedical data services. <br>
Mitigation: Avoid logging raw query strings and disclose that searches use external NCBI, NGDC, and CNGB endpoints. <br>


## Reference(s): <br>
- [Biomed Dataset Finder on ClawHub](https://clawhub.ai/gateswell/biomed-dataset-finder) <br>
- [NCBI E-utilities API Reference](references/ncbi_api.md) <br>
- [NGDC GSA API Reference](references/ngdc_api.md) <br>
- [CNGBdb API Reference](references/cngb_api.md) <br>
- [NCBI E-utilities](https://www.ncbi.nlm.nih.gov/home/develop/api/) <br>
- [NGDC](https://ngdc.cncb.ac.cn) <br>
- [CNGBdb](https://db.cngb.org) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown table with bold dataset IDs, article metadata, DOI links, and direct dataset links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dataset IDs and article details are expected to come from API responses; missing fields should remain blank rather than be filled from inference.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

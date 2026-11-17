## Description:

Search NCBI GEO/SRA, NGDC-GSA, and CNGB for biomedical datasets by disease, treatment, species, pathology subtype, and data type. Returns bold dataset ID, links, and article info in a structured table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gateswell](https://clawhub.ai/user/gateswell)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and analysts use this skill to find public biomedical datasets across NCBI GEO/SRA, NGDC-GSA, and CNGB from disease, treatment, species, subtype, and data type criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Biomedical search terms are sent to NCBI, NGDC, and CNGB.

Mitigation: Use the skill only when sending those search terms to the listed public dataset services is acceptable.

Risk: A CNGB token provided on the command line may be exposed through shell history, process listings, terminal logs, or job-runner metadata.

Mitigation: Prefer public-only search or skip CNGB when authenticated CNGB access is unnecessary; handle any token with appropriate local credential hygiene.

Risk: Incorrect or fabricated dataset identifiers and article metadata could mislead biomedical research work.

Mitigation: Use only dataset IDs and article fields returned by API responses, and leave missing response fields blank.

## Reference(s):

- [NCBI E-utilities API Reference](references/ncbi_api.md)
- [NGDC GSA API Reference](references/ngdc_api.md)
- [CNGBdb API Reference](references/cngb_api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown table with dataset identifiers, article metadata, DOI links, and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results must be grounded in returned API data; absent article fields are left blank rather than inferred.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

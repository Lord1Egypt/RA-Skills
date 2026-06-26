## Description: <br>
Query the ChEMBL database for bioactivity data on drug-like compounds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hollyya](https://clawhub.ai/user/hollyya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and drug discovery teams use this skill to query ChEMBL for target-based compound activity, molecule bioactivity profiles, and disease or indication drug records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Actual query execution depends on the surrounding OpenBioMed chembl_query implementation and may contact public ChEMBL services. <br>
Mitigation: Review the runtime implementation and avoid sending confidential compounds, targets, or disease terms to public services unless approved. <br>
Risk: Large or repeated ChEMBL lookups may hit public API rate limits or timeouts. <br>
Mitigation: Use the limit parameter, reduce broad queries, and retry with more specific target, molecule, or disease identifiers. <br>


## Reference(s): <br>
- [ChEMBL API Reference](artifact/references/api_endpoints.md) <br>
- [ChEMBL Web Services Documentation](https://chembl.gitbook.io/chembl-interface-documentation/web-resource-api) <br>
- [ChEMBL API Explorer](https://www.ebi.ac.uk/chembl/api/data/docs) <br>
- [ChEMBL Beaker Utility Services](https://chembl.gitbook.io/chembl-interface-documentation/chEMBL-beaker) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API Calls] <br>
**Output Format:** [Markdown with Python code snippets and tabular field descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns ChEMBL fields for target, molecule, and indication searches; result volume is controlled with the limit parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

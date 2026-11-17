## Description:

Query ChEMBL database for bioactivity data on drug-like compounds across target, molecule, and disease indication searches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hollyya](https://clawhub.ai/user/hollyya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to construct ChEMBL queries for target-based compound search, molecule bioactivity profiling, and disease indication drug lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries may contact the public ChEMBL service and disclose sensitive research terms.

Mitigation: Use the skill only with queries acceptable for public API disclosure, and avoid confidential project or compound information unless that sharing is approved.

## Reference(s):

- [ChEMBL API Reference](references/api_endpoints.md)
- [ChEMBL Web Services Documentation](https://chembl.gitbook.io/chembl-interface-documentation/web-resource-api)
- [ChEMBL API Explorer](https://www.ebi.ac.uk/chembl/api/data/docs)
- [ChEMBL Beaker Utility Services](https://chembl.gitbook.io/chembl-interface-documentation/chEMBL-beaker)

## Skill Output:

**Output Type(s):** [Guidance, Code, API Calls]

**Output Format:** [Markdown with Python code blocks and parameter tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides ChEMBL target, molecule, and indication queries; result size is controlled with the limit parameter.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

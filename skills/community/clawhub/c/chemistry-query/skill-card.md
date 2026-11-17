## Description:

Chemistry Query helps agents retrieve chemistry data from PubChem, ChEMBL, and PubMed and run RDKit-based molecular property, visualization, similarity, retrosynthesis, and reaction workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheminem](https://clawhub.ai/user/cheminem)

### License/Terms of Use:


## Use Case:

Developers and chemistry-focused agent users use this skill to look up compound data, compute molecular properties, generate molecule visualizations, search literature or bioactivity data, and draft synthesis or retrosynthesis outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Compound names, SMILES strings, or search terms may be sent to PubChem, ChEMBL, or PubMed.

Mitigation: Avoid submitting confidential compounds or sensitive search terms unless use of those external services is approved.

Risk: The optional Gradio UI is configured with public sharing enabled.

Mitigation: Run the UI only in trusted environments and disable public sharing before use beyond local review.

Risk: Generated molecule images and shared output paths can expose or overwrite prior analysis outputs.

Mitigation: Use isolated work directories and review generated output files before sharing or reusing them.

Risk: OPSIN support expects a separately obtained opsin.jar.

Mitigation: Install or execute the JAR only after verifying its source and checksum.

## Reference(s):

- [PubChem API endpoints reference](artifact/references/api_endpoints.md)
- [PubChem PUG REST documentation](https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest)
- [PubChem PUG REST API](https://pubchem.ncbi.nlm.nih.gov/rest/pug)
- [PubChem PUG View API](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view)
- [ChEMBL API data service](https://www.ebi.ac.uk/chembl/api/data)
- [NCBI Entrez E-utilities](https://eutils.ncbi.nlm.nih.gov/entrez/eutils)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Structured JSON with optional PNG or SVG molecule image files and command-oriented Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call external chemistry and literature services using compound names, SMILES strings, or search terms supplied by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata and release changelog; artifact documentation also mentions v1.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

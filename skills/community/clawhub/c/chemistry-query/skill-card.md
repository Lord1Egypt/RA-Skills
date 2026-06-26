## Description: <br>
Chemistry Query helps agents retrieve PubChem and related chemistry data, run RDKit molecule analysis, generate molecule visualizations, and plan or simulate chemistry workflows from compound names or SMILES. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cheminem](https://clawhub.ai/user/Cheminem) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and chemistry practitioners use this skill to query public compound data, calculate molecular properties, create structure images, and explore retrosynthesis or reaction workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compound names, SMILES strings, and related chemistry queries may be sent to public chemistry services. <br>
Mitigation: Use only inputs that are acceptable to disclose externally, and avoid submitting confidential chemistry data without an approved data-sharing path. <br>
Risk: The included Gradio UI can expose local processing through public sharing when run as provided. <br>
Mitigation: Disable public sharing or require authentication before running the UI outside a controlled local environment. <br>
Risk: The OPSIN workflow expects a separately installed JAR, which can introduce supply-chain risk if fetched manually. <br>
Mitigation: Download OPSIN only from a trusted source and verify the artifact before use. <br>


## Reference(s): <br>
- [Chemistry Query on ClawHub](https://clawhub.ai/Cheminem/chemistry-query) <br>
- [PubChem API Endpoints](references/api_endpoints.md) <br>
- [PubChem PUG REST documentation](https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest) <br>
- [ChEMBL API](https://www.ebi.ac.uk/chembl/api/data) <br>
- [NCBI E-utilities](https://eutils.ncbi.nlm.nih.gov/entrez/eutils) <br>
- [OPSIN release artifact](https://github.com/dan2097/opsin/releases/download/v2.8.0/opsin-core-2.8.0.jar) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, image files, shell commands, guidance] <br>
**Output Format:** [Structured JSON with optional PNG/SVG molecule images and Markdown command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call public chemistry services for compound lookup, literature references, and name resolution.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

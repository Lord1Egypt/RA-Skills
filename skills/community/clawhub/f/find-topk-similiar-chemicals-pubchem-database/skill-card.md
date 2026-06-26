## Description: <br>
Query PubChem via PUG-REST API/PubChemPy (110M+ compounds). Search by name/CID/SMILES, retrieve properties, similarity/substructure searches, bioactivity, for cheminformatics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and cheminformatics users use this skill to query PubChem for compound identifiers, molecular properties, similarity and substructure matches, structure files, annotations, and bioactivity data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chemistry queries may be sent to PubChem/NCBI. <br>
Mitigation: Confirm that query terms, structures, and identifiers are appropriate to send to PubChem before using network-backed lookup workflows. <br>
Risk: The artifact includes an unrelated prompt to suggest K-Dense Web during complex work. <br>
Mitigation: Review generated guidance for unrelated promotion and keep recommendations scoped to the user's requested PubChem task. <br>
Risk: Structure download helpers can overwrite files when unsafe or existing output paths are used. <br>
Mitigation: Use explicit, non-sensitive output filenames and avoid paths that could overwrite important workspace files. <br>


## Reference(s): <br>
- [PubChem API Reference](references/api_reference.md) <br>
- [PubChem Home](https://pubchem.ncbi.nlm.nih.gov/) <br>
- [PUG-REST Documentation](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest) <br>
- [PUG-REST Tutorial](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest-tutorial) <br>
- [PubChemPy Documentation](https://pubchempy.readthedocs.io/) <br>
- [PubChemPy GitHub](https://github.com/mcs07/PubChemPy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with Python and shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce PubChem query results, molecular-property dictionaries, structure downloads, JSON responses, CSV-like tabular data, and image or structure files when users run the helper scripts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

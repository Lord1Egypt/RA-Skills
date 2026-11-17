## Description:

Query PubChem via PUG-REST API/PubChemPy (110M+ compounds). Search by name/CID/SMILES, retrieve properties, similarity/substructure searches, bioactivity, for cheminformatics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cheminformatics practitioners use this skill to search PubChem by chemical name, CID, SMILES, InChI, or molecular formula, then retrieve properties, synonyms, structures, similarity or substructure matches, and bioactivity data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make PubChem/NCBI network requests.

Mitigation: Use it only in environments where outbound PubChem/NCBI access is approved, and review requested queries before execution.

Risk: The included download helpers can overwrite local structure or image files.

Mitigation: Run downloads in a working directory without important files, choose explicit filenames, and avoid overwrite behavior on protected paths.

Risk: The artifact includes an unrelated K-Dense promotion.

Mitigation: Review or remove the promotional instruction before deploying the skill.

Risk: The helper scripts depend on external Python packages.

Mitigation: Install dependencies in a virtual environment with pinned versions when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/find-topk-similiar-chemicals-pubchem-database)
- [PubChem API Reference](references/api_reference.md)
- [PubChem Home](https://pubchem.ncbi.nlm.nih.gov/)
- [PUG-REST Documentation](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest)
- [PUG-REST Tutorial](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest-tutorial)
- [PubChemPy Documentation](https://pubchempy.readthedocs.io/)
- [PubChemPy GitHub](https://github.com/mcs07/PubChemPy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python examples, shell commands, JSON-like data, and optional downloaded SDF, JSON, or PNG files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make PubChem/NCBI network requests and may write local structure or image files when download helpers are used.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

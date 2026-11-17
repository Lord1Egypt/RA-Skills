## Description:

Provides a small Python utility and usage guide for converting or validating common chemical identifiers such as names, SMILES strings, IUPAC names, and molecular formulas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cheminformatics practitioners can use this skill to produce guidance, code examples, and shell commands for small-scale chemical identifier lookup, SMILES syntax checks, and database standardization preparation; scientific results should be independently validated before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can overstate the accuracy of chemical conversion and SMILES validation.

Mitigation: Treat outputs as lookup or formatting assistance only and validate structures with trusted cheminformatics tools before scientific, safety, or drug-discovery use.

Risk: The artifact describes workflows that write local files without clear up-front disclosure.

Mitigation: Review proposed output paths and file-writing commands before execution, and run the skill with only the filesystem permissions needed for the intended workspace.

Risk: The bundled converter relies on a small local mock compound database.

Mitigation: Use authoritative external databases or curated internal references for compounds outside the small built-in examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/chemical-structure-converter)
- [PubChem](https://pubchem.ncbi.nlm.nih.gov)
- [ChemSpider](http://www.chemspider.com)
- [OpenSMILES](http://opensmiles.org)
- [InChI Trust](https://www.inchi-trust.org)
- [RDKit Documentation](https://www.rdkit.org/docs/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include suggested local CSV, JSON, or report filenames; chemical conversions and validation results require independent cheminformatics verification.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

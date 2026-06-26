## Description: <br>
Convert between IUPAC names, SMILES strings, and molecular formulas for chemical compounds. Supports structure validation, identifier interconversion, and cheminformatics data preparation for drug discovery and chemical research workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cheminformatics researchers use this skill to convert, validate, and standardize chemical identifiers for compound libraries, database registration, and research data preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chemical conversions may be incomplete or inaccurate because the bundled implementation uses a limited local compound database and basic SMILES checks. <br>
Mitigation: Verify outputs with trusted cheminformatics tools or institutional databases before using them for research, safety, inventory, or regulatory decisions. <br>
Risk: The skill can ask the agent to run local Python and create files such as CSV or JSON, while the documentation understates file access. <br>
Mitigation: Run it in a controlled workspace and review proposed commands and output paths before allowing file creation. <br>


## Reference(s): <br>
- [Chemical Structure Converter on ClawHub](https://clawhub.ai/AIPOCH-AI/chemical-structure-converter) <br>
- [PubChem](https://pubchem.ncbi.nlm.nih.gov) <br>
- [ChemSpider](http://www.chemspider.com) <br>
- [OpenSMILES Specification](http://opensmiles.org) <br>
- [InChI Standard](https://www.inchi-trust.org) <br>
- [RDKit Documentation](https://www.rdkit.org/docs/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell examples; optional CSV or JSON file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chemical results should be independently verified before research, safety, inventory, or regulatory use.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

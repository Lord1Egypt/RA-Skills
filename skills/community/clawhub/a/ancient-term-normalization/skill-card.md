## Description: <br>
Normalizes recognized characters or words from ancient manuscripts and excavated texts by mapping them to standardized forms and writing normalized term JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aricgamma](https://clawhub.ai/user/aricgamma) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and humanities researchers use this skill after OCR or character recognition to expand ancient text terms into aliases and standardized forms for search, retrieval, and downstream evidence workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The normalization script writes normalized_terms.json under term_normalisation in the chosen workspace, which can replace an existing output file. <br>
Mitigation: Run it in a dedicated workspace or back up an existing term_normalisation/normalized_terms.json before execution. <br>
Risk: Normalization quality depends on the provided recognition JSON and the bundled alias mapping. <br>
Mitigation: Review the generated normalized_terms.json before using it for search, retrieval, or evidence-chain decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aricgamma/ancient-term-normalization) <br>
- [Reference documentation](artifact/references/REFERENCE.md) <br>
- [Workflow](artifact/references/WORKFLOW.md) <br>
- [Recognized characters input schema](artifact/assets/schemas/recognized_chars.schema.json) <br>
- [Normalized terms output schema](artifact/assets/schemas/normalized_terms.schema.json) <br>
- [Historical aliases mapping](artifact/assets/data/historical_aliases.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [json, shell commands, guidance] <br>
**Output Format:** [JSON file plus concise command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes term_normalisation/normalized_terms.json in the selected workspace.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

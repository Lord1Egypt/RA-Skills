## Description: <br>
Build digital twin patient models to test drug efficacy and toxicity in virtual environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to build virtual patient models from genotype, clinical, and imaging JSON data and simulate drug efficacy, toxicity, and dose optimization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive patient-like genotype, clinical, and imaging data. <br>
Mitigation: Use synthetic or de-identified data unless appropriate authorization and privacy controls are in place. <br>
Risk: The skill produces dosing, efficacy, and toxicity-style outputs that could be mistaken for clinical guidance. <br>
Mitigation: Treat outputs as research simulations only and require qualified clinical review before any real-world decision-making. <br>
Risk: The skill runs Python code with dependencies and reads or writes local JSON files. <br>
Mitigation: Install and run it in an isolated environment, pin and review dependencies, and restrict input and output paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIPOCH-AI/digital-twin-patient-builder) <br>
- [Publisher profile](https://clawhub.ai/user/AIPOCH-AI) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [Artifact implementation](artifact/scripts/main.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, code, shell commands] <br>
**Output Format:** [JSON simulation results with terminal summaries and Python API return dictionaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires patient and drug profile JSON inputs; may write simulation results to a local JSON file.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and target metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

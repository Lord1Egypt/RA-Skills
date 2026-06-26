## Description: <br>
Design multicolor flow cytometry panels minimizing spectral overlap. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to draft multicolor flow cytometry marker-fluorophore assignments, estimate spectral overlap, and identify compensation needs. The output should be treated as a planning aid rather than validated laboratory guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The panel design output is a simplified planning aid and may not reflect validated laboratory performance. <br>
Mitigation: Review assignments, overlap estimates, and compensation recommendations with appropriate laboratory validation before use. <br>
Risk: Some documented CLI options are not implemented by the artifact script. <br>
Mitigation: Use the implemented options shown by the script help and verify expected behavior before relying on generated output. <br>
Risk: The skill executes a local Python script. <br>
Mitigation: Run it in a controlled workspace after reviewing the script and its inputs. <br>


## Reference(s): <br>
- [Flow Panel Designer on ClawHub](https://clawhub.ai/AIPOCH-AI/flow-panel-designer) <br>
- [AIPOCH-AI publisher profile](https://clawhub.ai/user/AIPOCH-AI) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text panel assignments with overlap and compensation notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No extra Python packages required; output is a simplified planning aid.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

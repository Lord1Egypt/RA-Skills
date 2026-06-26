## Description: <br>
ADMET and pharmacokinetic/pharmacodynamic property prediction workflows using ADMET Predictor, AOMP, OBA, Graph-pKa, DeepEsol, and Molecular Descriptors through SciMiner. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sciminer](https://clawhub.ai/user/sciminer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and computational chemistry teams use this skill to select and run SciMiner ADMET, PK/PD, pKa, solvation, metabolism, oral bioavailability, and molecular descriptor workflows for small-molecule assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a local SciMiner API key and sends authenticated requests to SciMiner. <br>
Mitigation: Keep the API key only in ~/.config/sciminer/credentials.json, never print or persist it, and send it only as the documented authentication header. <br>
Risk: Molecule data or uploaded files may be sent to SciMiner for prediction. <br>
Mitigation: Use the skill only with data the user is authorized to submit to SciMiner, and review the selected tool documentation before each invocation. <br>


## Reference(s): <br>
- [SciMiner tool API documentation](https://sciminer.tech/tool_api_files/) <br>
- [SciMiner API key utility](https://sciminer.tech/utility) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, text] <br>
**Output Format:** [Markdown guidance with generated invocation code or shell commands and SciMiner task share URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task IDs, status summaries, JSON result excerpts, and share_url links returned by SciMiner.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

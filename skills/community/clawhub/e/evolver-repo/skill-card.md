## Description: <br>
A self-evolution engine for AI agents that analyzes runtime history to identify improvements and applies protocol-constrained evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WuZiMaKi](https://clawhub.ai/user/WuZiMaKi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent teams use this skill to inspect agent runtime history, identify failures or inefficiencies, and produce protocol-bound evolution guidance, assets, and validation steps for review or application. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is marked suspicious because it performs under-disclosed auto-updates, default Hub networking, persistent node identification, and externally influenced task handling. <br>
Mitigation: Install only after review, constrain execution, disable or block network egress when Hub contact is not desired, and turn off auto-update in OpenClaw config before normal use. <br>
Risk: Continuous or automated evolution can run as a background worker and produce repeated changes without enough operator attention. <br>
Mitigation: Use review or dry-run modes first, avoid --loop unless continuous operation is intended, and run initial evaluations in a disposable git repository. <br>
Risk: Command-bearing environment variables can expand the local command surface. <br>
Mitigation: Avoid setting command-bearing variables such as INTEGRATION_STATUS_CMD and run without sensitive session history or credentials. <br>


## Reference(s): <br>
- [Evolver Repo on ClawHub](https://clawhub.ai/WuZiMaKi/evolver-repo) <br>
- [EvoMap](https://evomap.ai) <br>
- [EvoMap Documentation](https://evomap.ai/wiki) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured GEP assets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local evolution assets, events, and validation reports when executed in a workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

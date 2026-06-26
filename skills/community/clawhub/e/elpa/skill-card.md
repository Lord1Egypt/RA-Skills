## Description: <br>
Orchestrate real ELPA-style ensemble forecasting workflows by triggering external sub-model training jobs (for example PyTorch/Prophet/TiDE/transformers), then computing ELPA online/offline weights from validation errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AnonymousCodeMaker](https://clawhub.ai/user/AnonymousCodeMaker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ML engineers use this skill to plan and run multi-model forecasting training workflows, then build ELPA ensemble policy JSON from validation errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Execute mode runs training commands from the user's configuration on the local machine. <br>
Mitigation: Start with dry-run mode, inspect every rendered train_cmd, use trusted configs and training code only, and run without unnecessary secrets or elevated privileges. <br>


## Reference(s): <br>
- [ELPA Config Schema](references/config-schema.md) <br>
- [ClawHub ELPA Release](https://clawhub.ai/AnonymousCodeMaker/elpa) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON configuration and policy files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run mode writes a training manifest; integration writes an ELPA policy JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Evaluates agent outputs for correctness, clarity, completeness, and safety, providing numeric scores and detailed feedback for quality control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Wang-ErQian](https://clawhub.ai/user/Wang-ErQian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent-workflow builders use this skill to add a critic step that reviews another agent's output, assigns weighted quality scores, and returns actionable suggestions before delivery or retry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reviewed tasks and agent outputs may contain secrets, customer data, proprietary code, or regulated information that could be sent to a model provider or retained in critique logs. <br>
Mitigation: Configure the model/provider deliberately, avoid sending sensitive content unless that provider is acceptable, and log only minimal or redacted critique data with a clear retention policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Wang-ErQian/critic-agent) <br>
- [Configuration Reference](artifact/references/configuration.md) <br>
- [Integration Patterns](artifact/references/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Structured JSON critique with numeric scores, per-dimension feedback, an overall assessment, and suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a weighted rubric: correctness 40%, clarity 25%, completeness 25%, and safety 10%.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

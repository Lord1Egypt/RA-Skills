## Description: <br>
Helps an agent query user-owned biometric, blood-panel, supplement, nutrition, and body-composition data from a local Biohub setup for wellness and recovery analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxnau89](https://clawhub.ai/user/maxnau89) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to answer wellness, recovery, training-readiness, blood-work, supplement, nutrition, and body-composition questions grounded in local user-owned data. It is not medical advice and should not be used to diagnose conditions or prescribe treatment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent access to sensitive local biometric and health records. <br>
Mitigation: Install only when that access is intended, ask explicit questions about the metric and timeframe to analyze, and review any workspace memory the agent creates. <br>
Risk: Wellness analysis could be mistaken for medical advice. <br>
Mitigation: Treat outputs as wellness context only; do not use the skill to diagnose conditions, prescribe treatment, or replace clinician guidance. <br>
Risk: Workspace-local memory can capture sensitive health details. <br>
Mitigation: Keep memory files local, review them periodically, and do not commit or package user-identifying biometric data. <br>


## Reference(s): <br>
- [ClawHub Biohub listing](https://clawhub.ai/maxnau89/biohub) <br>
- [Project homepage](https://github.com/maxnau89/openclaw-biohub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with SQL examples, shell commands, and wellness-analysis guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local SQLite health data and workspace-local memory; outputs should avoid committing or publishing user-identifying biometric data.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

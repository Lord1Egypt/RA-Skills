## Description: <br>
Provides model-routing guidance that keeps simple Q&A and routine tasks on Haiku 4.5 while escalating analysis, coding, planning, deep research, and critical decisions to stronger Claude models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axellageraldinc](https://clawhub.ai/user/axellageraldinc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agent operators and developers use this skill to choose an appropriate Claude model for each request, reserving stronger and potentially more expensive models for reasoning-heavy or critical tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The routing guidance may send complex tasks to stronger and potentially more expensive models. <br>
Mitigation: Review the model-selection rules before use in sensitive or cost-controlled workflows. <br>
Risk: The skill provides routing instructions rather than deterministic enforcement, so agents may still choose an unsuitable model. <br>
Mitigation: Review outputs for the declared model choice and apply local policy when a request is critical or cost-sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/axellageraldinc/claude-hemat) <br>
- [Publisher profile](https://clawhub.ai/user/axellageraldinc) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text] <br>
**Output Format:** [Markdown guidance with model-routing rules and example session-spawn calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should state which model was used and return to Haiku 4.5 after escalated work.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Turn a feature idea into a concrete technical implementation plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzfshark](https://clawhub.ai/user/mzfshark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn feature ideas, architecture requests, and multi-component changes into implementation plans covering modules, interfaces, data flow, validation, rollout, and open questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Malformed activation metadata can make automatic invocation behavior unclear. <br>
Mitigation: Replace the malformed System.Object[] trigger with explicit implementation-planning activation phrases before relying on automatic invocation. <br>
Risk: Implementation plans can propose changes that do not fit a user's production constraints. <br>
Mitigation: Review plans against stated constraints and require explicit gating for any deployment path that could affect production. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mzfshark/axodus-implementation-planner) <br>
- [Publisher profile](https://clawhub.ai/user/mzfshark) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Structured Markdown plan with YAML-style examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Plans may include architecture, modules, interfaces, validation steps, rollout guardrails, and open questions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.yml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

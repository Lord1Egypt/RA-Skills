## Description: <br>
Provides a quantitative agent evaluation framework with yes/no checklists, scoring tiers, recurring self-review, and improvement loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luaqnyin](https://clawhub.ai/user/luaqnyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and team leads use this skill to define quantifiable yes/no evaluations for specialized agents, score historical tasks, and route failures into improvement loops. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring evaluation of historical task logs can expose sensitive task details. <br>
Mitigation: Set explicit allowed memory paths and review sensitive records before evaluation. <br>
Risk: Persistent improvement records can create unintended memory writes. <br>
Mitigation: Require confirmation before writing evaluation results, patterns, or agent evolution records. <br>
Risk: Scheduled reports can send performance or task details to unintended recipients. <br>
Mitigation: Define approved recipients before enabling scheduled reports and avoid sharing sensitive details without review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luaqnyin/agent-eval) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance with checklists, scoring rules, and scheduled workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces evaluation criteria, score thresholds, memory update patterns, and reporting workflow guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

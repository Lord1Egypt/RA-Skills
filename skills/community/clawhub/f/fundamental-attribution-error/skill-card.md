## Description: <br>
Helps agents audit character-based explanations for behavior by testing dispositional claims against situational alternatives, actor-observer asymmetry, and calibrated intervention choices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, managers, product teams, incident reviewers, and other decision makers use this skill to examine whether a judgment over-weights character explanations and under-weights situational causes before making coaching, churn, post-mortem, conflict, or product decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may over-correct toward situational explanations and weaken warranted accountability. <br>
Mitigation: Use the documented fit check: if behavior is verified across many distinct situations, treat dispositional inference as stronger and keep accountability tied to controllable behavior. <br>
Risk: A user may treat the audit as a definitive psychological assessment rather than a decision aid. <br>
Mitigation: Use the output as calibrated reasoning guidance, document assumptions, and schedule the skill's recommended re-evaluation point after situational interventions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/deciqai/skills/fundamental-attribution-error) <br>
- [Sources - fundamental-attribution-error](references/sources.md) <br>
- [Method in Action: Jones-Harris 1967 Castro Study + Ross 1977 Synthesis + Modern Applications](examples/jones-harris-1967-castro-study-ross-1977-synthesis-modern-applications.md) <br>
- [deciqAI](https://deciqai.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text] <br>
**Output Format:** [Markdown with a structured FAE Audit template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask stepwise coaching questions and wait for user input when the user has no concrete case or is unfamiliar with the concept.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

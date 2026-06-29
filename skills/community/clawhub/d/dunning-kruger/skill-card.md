## Description: <br>
Helps agents diagnose and coach around miscalibrated self-assessment by testing confidence claims against external performance data and feedback loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and decision-makers use this skill to evaluate overconfident or underconfident self-assessments in domains such as hiring, promotion, programming, investing, medicine, and expert review. It guides the agent to collect external evidence, compare self-assessed and measured performance, and propose calibration or feedback interventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be misapplied to high-stakes people decisions when confidence claims are not backed by external performance data. <br>
Mitigation: Require measurable evidence, expert evaluation, or structured review before using the diagnosis to support hiring, promotion, medical, financial, or similar decisions. <br>
Risk: A diagnosis based on incomplete evidence can produce misleading calibration guidance. <br>
Mitigation: Use the skill's verification checklist to document the claim, available external data, metacognitive test, quartile diagnosis, intervention, and re-measurement plan. <br>


## Reference(s): <br>
- [Primary sources for dunning-kruger](references/sources.md) <br>
- [Kruger and Dunning's 1999 Cornell Studies](examples/kruger-and-dunnings-1999-cornell-studies.md) <br>
- [ClawHub skill page](https://clawhub.ai/deciqai/skills/dunning-kruger) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown diagnosis and coaching guidance with structured fields and follow-up questions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only output; no API calls, shell commands, credentials, or tool integrations were detected in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

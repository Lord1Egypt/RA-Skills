## Description: <br>
Generates Dify 1.3.1-compatible Agent workflow YAML from business requirements, SOPs, or workflow descriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevsimba](https://clawhub.ai/user/kevsimba) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workflow builders use this skill to convert business process descriptions or SOPs into Dify 1.3.1 workflow or advanced-chat YAML that can be reviewed and imported into Dify. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may paste confidential SOPs or operational process details into the agent. <br>
Mitigation: Use only content approved for the target agent environment and redact sensitive operational details when possible. <br>
Risk: Generated YAML may encode an incorrect workflow or unsuitable automation behavior. <br>
Mitigation: Review the generated YAML before importing it into Dify and test it with representative inputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kevsimba/agentymlgenerator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with a workflow summary, YAML code block, and import guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [YAML is intended for Dify 1.3.1 import after human review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

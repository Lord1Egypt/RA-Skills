## Description: <br>
Code Review Pro guides an agent to perform parallel code review across logic, security, performance, and style, reporting findings at a stated confidence threshold of 70% or higher. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[softboypatrick](https://clawhub.ai/user/softboypatrick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to request structured code review feedback on logical errors, security vulnerabilities, performance bottlenecks, and style issues. It is intended to produce concise findings with severity, confidence, location, risk level, and suggested fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's confidence scores are advisory and are not backed by an independent verifier. <br>
Mitigation: Treat findings as review guidance and have a qualified developer confirm any reported issue before acting on it. <br>
Risk: Code review requests may include sensitive proprietary code. <br>
Mitigation: Avoid sharing sensitive code unless the agent environment is approved for that material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/softboypatrick/code-review-pro) <br>
- [Publisher profile](https://clawhub.ai/user/softboypatrick) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown review findings with severity, confidence, location, risk, and suggested remediation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports only severe issues or optimization suggestions that meet the skill's stated confidence threshold of 70% or higher.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

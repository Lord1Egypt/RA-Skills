## Description: <br>
代码审查助手，帮助用户审查提交的代码，识别代码质量、潜在 Bug、性能、安全漏洞和可维护性问题。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[olina1ye](https://clawhub.ai/user/olina1ye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and reviewers use this skill to get Chinese-language PR and code review feedback, including prioritized issues, performance and security risks, maintainability concerns, and suggested fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read code or repository files provided for review, including private or unrelated files if invoked too broadly. <br>
Mitigation: Invoke it only on files intended for review and avoid including private, sensitive, or unrelated repository content unless that content should be part of the review. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown review feedback with prioritized issue lists and optional code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language output; reviews only code the user asks the agent to read.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

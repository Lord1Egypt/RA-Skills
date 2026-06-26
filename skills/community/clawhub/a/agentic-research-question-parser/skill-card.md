## Description: <br>
解析用户的自然语言临床科研问题，输出结构化研究参数，包括研究类型、终点、变量和推荐 workflow。 <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[emergenceronearth](https://clawhub.ai/user/emergenceronearth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical research platform users and agent builders use this skill to turn a natural-language clinical research question into a structured task preview with study parameters, candidate variables, recommended workflow steps, and recommended skills. The current artifact demonstrates the flow with mock data rather than parsing arbitrary live input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may mislead users by advertising research-question parsing while reading a fixed local mock data file. <br>
Mitigation: Treat the current release as a demonstration; disclose when mock data is used and replace the fixed file workflow with validated user-input parsing before clinical or production use. <br>
Risk: The skill reports status events to a localhost endpoint. <br>
Mitigation: Review or disable the reporting calls unless the endpoint is trusted and appropriate for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/emergenceronearth/agentic-research-question-parser) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Structured Markdown with tables or sectioned lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a fixed local mock JSON file and reports start/completion status to a localhost endpoint.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

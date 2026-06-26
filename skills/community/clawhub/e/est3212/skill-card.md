## Description: <br>
在任何创造性工作之前必须使用 - 创建功能、构建组件、添加新功能或修改行为。通过协作对话探索用户意图、需求和设计。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lky115](https://clawhub.ai/user/lky115) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and builders use this skill before creative or implementation work to turn a vague idea into a validated design through focused questions, alternatives, and section-by-section review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect project files and git history to understand the current workspace. <br>
Mitigation: Use it in the intended project workspace and avoid running it where the agent should not inspect local context. <br>
Risk: The skill may create a design document and commit it after the design is approved. <br>
Mitigation: Review the generated design document and approve any git action explicitly before relying on the result. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Files] <br>
**Output Format:** [Conversational text and Markdown design documents] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a docs/plans design document and prepare a git commit after the user validates the design.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description:

深度思考协议增强 AI 助手在复杂问题、技术难题、战略决策、复杂系统设计和多利益相关者场景中的分析、推理、假设检验和综合判断能力。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hejng](https://clawhub.ai/user/hejng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external agent users use this skill to guide structured reasoning for complex analysis, technical design, strategic decisions, debugging, and other high-value questions. It provides a staged thinking framework, quick reference material, examples, and an optional checklist script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to expose detailed private reasoning, which can reveal unnecessary internal deliberation or sensitive context.

Mitigation: Revise operating instructions to keep reasoning private, provide concise rationale, declare tool scope, and avoid exposing hidden chain-of-thought.

Risk: The optional checklist script collects problem descriptions, stakeholders, constraints, and success criteria interactively.

Mitigation: Review entered information for sensitivity and avoid supplying secrets, credentials, personal data, or confidential business details.

## Reference(s):

- [Deep Thinking Protocol Examples](references/examples.md)
- [Deep Thinking Protocol Quick Reference](references/quick-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/hejng/skills/deep-thinking-protocol)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional code or shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The optional checklist script can print prompts and structured checklist text during interactive use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

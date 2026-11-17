## Description:

根据指定的Java接口（Controller方法/API路径）分析完整调用链路，生成Mermaid时序图，标注关键判断节点、异常处理分支和业务逻辑。当用户要求分析接口调用链路、生成时序图、分析接口流程、查看接口调用关系时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijie012](https://clawhub.ai/user/lijie012)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to trace Java API call chains from a Controller method, API path, or Service method and produce Mermaid sequence diagrams with key decision points, exception branches, and call-chain details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose repository implementation details while summarizing Java API call paths and generating diagrams.

Mitigation: Use it only on code that may be included in the agent conversation or output, and avoid running it on repositories whose implementation details should not be shared in that context.

Risk: Generated call-chain analysis and Mermaid diagrams may omit or misstate behavior in complex Java projects.

Mitigation: Review the generated diagram, decision-node table, and call-chain details against the source code before using them for engineering decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lijie012/skills/api-sequence-diagram)
- [Publisher Profile](https://clawhub.ai/user/lijie012)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with Mermaid sequenceDiagram code blocks and analysis tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include interface summaries, sequence diagrams, decision-node tables, call-chain details, transaction notes, exception handling notes, performance concerns, and external dependency notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

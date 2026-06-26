## Description: <br>
Conversation Focus is a Chinese-language clarification workflow that analyzes user intent, asks focused follow-up questions when needs or constraints are vague, and consolidates clarified requirements into a clean task context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[as1113435](https://clawhub.ai/user/as1113435) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to keep conversations focused by clarifying goals, constraints, and success criteria before execution. It is most useful for vague requests, multi-step tasks, or conversations that need to be brought back on topic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may log clarified requests to a local self-improvement record, which could capture sensitive personal, business, or credential-like content. <br>
Mitigation: Review or disable the self-improving/corrections.md logging behavior before using the skill with sensitive content. <br>
Risk: The skill references companion components such as self-improving, thought-retriever, and prompt-optimizer-chinese that are not included in this artifact. <br>
Mitigation: Assess and trust those companion components separately before enabling integrations that depend on them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text] <br>
**Output Format:** [Markdown and plain-language clarification prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce structured task context with goals, constraints, and success criteria.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

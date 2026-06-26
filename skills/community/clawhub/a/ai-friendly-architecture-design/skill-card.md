## Description: <br>
Use when a system needs to handle AI uncertainty, select agent types, expose APIs for AI agents, or support probabilistic outputs and dynamic planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ganjiakoun16](https://clawhub.ai/user/ganjiakoun16) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to decide when AI-friendly architecture is appropriate and to design LLM or agent-based systems with model management, context engineering, AI-friendly APIs, evaluation, and fallback patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Architecture guidance could be applied directly to high-stakes systems without adequate review, especially where autonomous agents, persistent memory, or external model providers are involved. <br>
Mitigation: Review recommendations with domain, security, privacy, and safety stakeholders before implementation; add validation, fallback, and monitoring controls for production use. <br>
Risk: The skill may encourage unnecessary AI or multi-agent complexity for deterministic workflows. <br>
Mitigation: Apply the included decision framework and explicit do-not-use guidance before selecting AI-friendly architecture. <br>
Risk: Illustrative performance and accuracy examples may not transfer to a new domain. <br>
Mitigation: Run domain-specific evaluations and treat the included metrics as examples rather than guaranteed outcomes. <br>
Risk: The included eval runner is executable code. <br>
Mitigation: Run the eval script only when testing skill behavior and review its behavior before execution. <br>


## Reference(s): <br>
- [Article Summary](references/article-summary.md) <br>
- [Evaluation Criteria](references/evals.md) <br>
- [Test Scenarios](references/test-scenarios.md) <br>
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands] <br>
**Output Format:** [Markdown guidance with architecture tables, decision frameworks, code examples, and optional shell commands for evaluations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory architecture recommendations; includes optional evaluation runner guidance but does not provide a runtime AI framework.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

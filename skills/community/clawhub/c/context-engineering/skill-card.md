## Description: <br>
Provides guidance for compressing long-running agent context with structured summaries, evaluation probes, and token-per-task optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leoyessi10-tech](https://clawhub.ai/user/leoyessi10-tech) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to design, evaluate, and debug context-compression workflows for long-running agent sessions and large codebase work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compressed summaries may preserve sensitive conversation details such as file paths, user goals, decisions, and excerpts from prior context. <br>
Mitigation: Review and redact summaries before storing them outside the active workspace or sharing them with another system. <br>
Risk: Adapting the optional LLM-judge evaluation flow may send compressed context to an external model provider. <br>
Mitigation: Use approved model providers and redact sensitive content before external evaluation. <br>
Risk: Compression can omit artifact-tracking details that an agent needs to continue work accurately. <br>
Mitigation: Use explicit file and decision sections, and review generated summaries before relying on them for follow-up work. <br>


## Reference(s): <br>
- [Context Compression Evaluation Framework](references/evaluation-framework.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/leoyessi10-tech/context-engineering) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code] <br>
**Output Format:** [Markdown guidance with optional Python evaluation utilities] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured summary templates, compression evaluation criteria, and recommendations for preserving artifact trails.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

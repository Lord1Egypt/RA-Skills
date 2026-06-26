## Description: <br>
Guides agents and engineers to split multi-call language-model workflows by cognitive load, using strong models for reasoning decisions and cheaper models for frequent execution steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentsope](https://clawhub.ai/user/agentsope) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill when designing or cost-optimizing multi-call language-model pipelines, deciding which steps need a strong reasoner versus a cheap executor, and adding escalation when a cheap tier degrades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Model prices, capabilities, and benchmark results can become stale. <br>
Mitigation: Re-measure cost, latency, and quality on the target workflow before relying on a recommended split. <br>
Risk: A cheap execution tier can produce invalid formats or lower-quality outputs on long-tail inputs. <br>
Mitigation: Use detectable failure signals such as schema validation, tests, or self-checks, then escalate failed steps to the stronger tier. <br>
Risk: The release has low trust-tier evidence despite passing quality and security checks. <br>
Mitigation: Review the documentation and cited sources before adopting the guidance in production planning. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentsope/agentsop-cost-tiered-models) <br>
- [Aider Architect Mode](https://aider.chat/2024/09/26/architect.html) <br>
- [DSPy Optimizer and Task Model Discussion](https://github.com/stanfordnlp/dspy/issues/1596) <br>
- [vLLM Speculative Decoding](https://docs.vllm.ai/en/latest/features/speculative_decoding/) <br>
- [LangGraph Multi-Agent Concepts](https://langchain-ai.github.io/langgraph/concepts/multi_agent/) <br>
- [Source Evidence Reference](references/R1-source-evidence.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with decision tables and workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; produces planning guidance rather than executable actions.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

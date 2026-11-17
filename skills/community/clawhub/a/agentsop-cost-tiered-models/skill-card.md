## Description:

Guides agents and engineers in splitting multi-call LM workflows by cognitive load, using stronger models for scarce reasoning decisions and cheaper models for frequent mechanical execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentsope](https://clawhub.ai/user/agentsope)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when designing or cost-optimizing multi-call LM pipelines. It helps assign stronger models to planning, routing, judging, and fallback decisions while assigning cheaper models to repetitive rewrite, extraction, formatting, application, and draft steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cost and quality recommendations may not transfer to a user's own workload or current model lineup.

Mitigation: Re-measure quality delta, cost delta, and latency on representative tasks before adopting a split.

Risk: A cheaper execution-tier model can produce invalid formats, failed tests, or lower-quality outputs on long-tail inputs.

Mitigation: Add detectable failure checks and escalate failed steps to a stronger model or a more robust output format.

Risk: The skill is Chinese-heavy, which may reduce reviewability for teams that require English-only operational guidance.

Mitigation: Have a qualified reviewer confirm the guidance and examples before applying them in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentsope/skills/agentsop-cost-tiered-models)
- [Source evidence](references/R1-source-evidence.md)
- [Aider architect mode](https://aider.chat/2024/09/26/architect.html)
- [DSPy optimizer and task model discussion](https://github.com/stanfordnlp/dspy/issues/1596)
- [vLLM speculative decoding](https://docs.vllm.ai/en/latest/features/speculative_decoding/)
- [LangGraph multi-agent concepts](https://langchain-ai.github.io/langgraph/concepts/multi_agent/)
- [Aider edit error handling](https://aider.chat/docs/troubleshooting/edit-errors.html)
- [Aider code in JSON analysis](https://aider.chat/2024/08/14/code-in-json.html)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with decision rules, mapping tables, and escalation checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; no hidden execution, data access, or persistence.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

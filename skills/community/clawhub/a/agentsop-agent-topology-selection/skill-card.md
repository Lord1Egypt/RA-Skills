## Description: <br>
Cross-framework enhancement overlay that helps an agent decide whether a task needs multiple agents and, if so, choose between single-agent, sequential, supervisor, swarm, or hierarchical topologies before implementation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentsope](https://clawhub.ai/user/agentsope) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill during multi-agent planning to defend the single-agent baseline, identify when role splitting is justified, and select an appropriate topology across CrewAI, LangGraph, and OpenAI Swarm-style handoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The overlay may activate during broad multi-agent design discussions and influence architecture choices outside a narrow implementation task. <br>
Mitigation: Treat its output as planning guidance and review topology changes against the project's trust, latency, cost, and audit requirements before implementation. <br>
Risk: The release evidence notes local authoring paths in metadata or source-evidence text. <br>
Mitigation: Use those paths only as provenance notes for this release and remove local machine paths from future public releases. <br>
Risk: Incorrect multi-agent topology choices can add unnecessary agents, token cost, latency, or unbounded handoff loops. <br>
Mitigation: Apply the single-agent baseline first, require a concrete split-justifying failure mode, and bound runtime handoff topologies with iteration limits, timeouts, and explicit exit state. <br>


## Reference(s): <br>
- [R1 Source Evidence](artifact/references/R1-source-evidence.md) <br>
- [Operation Candidates](artifact/intermediate/operation_candidates.json) <br>
- [LangChain Benchmarking Multi-Agent Architectures](https://www.langchain.com/blog/benchmarking-multi-agent-architectures) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with topology rubrics, decision steps, anti-patterns, and framework mapping notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory planning output; does not execute tools or modify files.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata; artifact frontmatter is 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description:

Cross-framework enhancement overlay for deciding whether an agent task needs multiple agents and, if so, choosing single-agent, sequential, supervisor, swarm, or hierarchical topology using a binary-question rubric.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentsope](https://clawhub.ai/user/agentsope)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill before writing agent code to decide whether a single agent with tools is sufficient or whether a multi-agent topology is justified. When multiple agents are justified, it guides selection among sequential, supervisor, swarm, and hierarchical patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact documentation includes publisher-local source paths.

Mitigation: Treat those paths as provenance notes only; do not rely on them as install-time or runtime paths.

Risk: Topology guidance can be misapplied to create unnecessary multi-agent systems with higher latency, token use, or coordination risk.

Mitigation: Apply the skill's single-agent baseline check first and add agents only when context isolation or parallel expertise is clearly justified.

Risk: Runtime handoff topologies can loop or fail to terminate if delegation is left unbounded.

Mitigation: Use explicit iteration limits, outer timeouts, and state-based exit counters before deploying supervisor, swarm, hierarchical, or delegation-heavy designs.

## Reference(s):

- [Source Evidence](artifact/references/R1-source-evidence.md)
- [LangChain Benchmarking Multi-Agent Architectures](https://www.langchain.com/blog/benchmarking-multi-agent-architectures)
- [ClawHub Skill Page](https://clawhub.ai/agentsope/skills/agentsop-agent-topology-selection)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with rubrics, topology mappings, and implementation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; produces topology-selection recommendations and implementation guardrails.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter is 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

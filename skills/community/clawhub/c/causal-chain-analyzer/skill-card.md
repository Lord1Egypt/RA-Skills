## Description:

Analyzes and traces cause-effect chains in knowledge graphs to identify root causes, downstream impacts, dependencies, cycles, and ranked causal paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fisa712](https://clawhub.ai/user/fisa712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and analysts use this skill to examine directed causal or dependency graphs, find likely root causes, trace downstream effects, detect feedback loops, and rank causal chains by proximity or confidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Very large or adversarial graph inputs can create high traversal cost or memory pressure.

Mitigation: Use bounded max_depth, max_results, confidence thresholds, and external runtime resource limits before analyzing untrusted graph data.

Risk: Causal-chain output can be incomplete or misleading if graph relationships, weights, or confidence values are incomplete or inaccurate.

Mitigation: Treat results as analytical guidance, validate causal assumptions with domain owners, and review findings before taking operational or remediation action.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fisa712/skills/causal-chain-analyzer)
- [OpenClaw Homepage](https://clawhub.com)
- [Causal Chain Analysis - Design Patterns & Algorithms](references/causal-chain-patterns.md)
- [Causal Chain Analysis - Real-World Examples](examples/causal-chain-examples.md)
- [CausalChainAnalyzer Python Helper](scripts/causal_chain_analyzer.py)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown guidance with Python code examples and JSON-serializable analysis results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include root-cause lists, causal paths, affected nodes, confidence scores, cycle findings, and chain statistics.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

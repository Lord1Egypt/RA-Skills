## Description: <br>
Analyze and trace cause-effect chains in knowledge graphs to identify root causes, downstream impacts, dependencies, cycles, and ranked causal paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fisa712](https://clawhub.ai/user/fisa712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge-graph practitioners, and operations teams use this skill to inspect user-provided causal graphs, find likely root causes, trace downstream effects, detect feedback loops, and rank candidate causal chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unneeded purchase, financial, credential, or broad data-access tools could expand agent authority beyond local graph analysis. <br>
Mitigation: Install it as a local graph-analysis aid and grant only the graph data and local execution access required for the task. <br>
Risk: Causal conclusions can be misleading when user-provided graph relationships, weights, or confidence scores are incomplete or incorrect. <br>
Mitigation: Review the input graph, thresholds, ranked chains, and cycle results before using outputs for operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fisa712/causal-chain-analyzer) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/fisa712) <br>
- [ClawHub homepage](https://clawhub.com) <br>
- [Causal chain patterns](references/causal-chain-patterns.md) <br>
- [Causal chain examples](examples/causal-chain-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown guidance with structured causal-analysis summaries and optional Python or JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on user-provided graph data, selected traversal settings, depth limits, confidence thresholds, and ranking strategy.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

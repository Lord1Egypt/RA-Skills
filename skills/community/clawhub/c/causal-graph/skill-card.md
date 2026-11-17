## Description:

Builds a local causal knowledge graph by extracting entities, dated events, and causal relationships from workspace memory and log files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weidadong2359](https://clawhub.ai/user/weidadong2359)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to turn workspace memory files, daily logs, and task notes into a causal graph for analysis, querying, and visualization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local memory and log files that may contain sensitive workspace information.

Mitigation: Review or redact MEMORY.md and memory logs before use, as recommended by the server security guidance.

Risk: The documented LLM extraction option may send memory text to a model provider if enabled.

Mitigation: Use the local rule-based flow by default, and enable LLM extraction only after confirming that the chosen provider may process the workspace text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weidadong2359/skills/causal-graph)
- [Publisher profile](https://clawhub.ai/user/weidadong2359)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command examples; runtime output includes console text and a JSON graph file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the generated graph to memory/causal-graph.json when executed in a workspace with matching memory files.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

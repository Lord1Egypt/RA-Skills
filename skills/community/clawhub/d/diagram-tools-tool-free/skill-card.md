## Description:

图表工具基础版 helps agents generate Mermaid and Graphviz diagrams, including flowcharts, sequence diagrams, mind maps, Gantt charts, and data charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, individual users, and workflow builders use this skill to turn natural-language diagram requests into Mermaid, Graphviz DOT, and related chart outputs for documentation or lightweight automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad automatic tool use and shell execution for diagram work.

Mitigation: Review generated commands before execution and run the skill in a least-privilege workspace with only the files needed for the diagram task.

Risk: Privacy and API-key handling are unclear, and some functions may use external APIs or network access.

Mitigation: Avoid sensitive diagrams, prompts, or secrets until the publisher clarifies which operations stay local, which services are contacted, and how credentials should be stored.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/diagram-tools-tool-free)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Mermaid, Graphviz DOT, JSON/text/csv examples, and inline shell or code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require tool-use and shell execution; the free edition is described as single-task oriented.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

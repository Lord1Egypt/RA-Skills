## Description: <br>
Deep Research Agent performs structured research and analysis on user-supplied topics, producing sourced summaries, reports, comparisons, landscape maps, and evaluation recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jahonn](https://clawhub.ai/user/jahonn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other external users use this skill to turn broad questions into sourced summaries, deep research reports, comparison matrices, landscape maps, and decision frameworks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research outputs may include incorrect, stale, biased, or incomplete source interpretations. <br>
Mitigation: Review cited sources, confidence notes, and gaps before using the output for decisions. <br>
Risk: The skill uses web search and may use subagent processing, which can expose sensitive internal information if prompts include it. <br>
Mitigation: Use scoped installation and avoid sensitive internal information unless web search and subagent processing are acceptable for the use case. <br>


## Reference(s): <br>
- [Research Agent Methodology Reference](references/methodology.md) <br>
- [Agent Skills](https://agentskills.io) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>
- [Deep Research Agent on ClawHub](https://clawhub.ai/jahonn/deep-research-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown research reports, comparison tables, decision matrices, and concise conversational summaries with sources.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write RESEARCH.md for deep dives or LANDSCAPE.md for longer landscape analyses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

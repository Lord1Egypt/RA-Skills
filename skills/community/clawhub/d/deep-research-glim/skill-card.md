## Description: <br>
Conducts deep, multi-angle research using glim MCP tools and parallel subagents for competitive landscape analysis, strategic intelligence, and multi-source synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers, analysts, and strategy teams use this skill to run structured deep research across multiple source types, validate claims across sources, and produce an evidence-rich synthesis for a requested topic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be triggered by ordinary phrases such as "deep research" or "deep dive on," which may start an external research workflow unintentionally. <br>
Mitigation: Confirm the intended research topic before broad source collection, especially when the prompt could include private or sensitive context. <br>
Risk: The workflow can spawn several subagents and query external sources, increasing exposure of the research topic and consuming more tool budget than a simple search. <br>
Mitigation: Avoid invoking it for sensitive topics unless external research is acceptable, and bound the source plan when cost or disclosure risk matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tenequm/deep-research-glim) <br>
- [Publisher profile](https://clawhub.ai/user/tenequm) <br>
- [OpenClaw homepage](https://github.com/tenequm/skills/tree/main/skills/deep-research-glim) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown research report with structured findings, citations, contradictions, strategic insights, metrics, and annotated sources.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use external research tools and parallel subagents to gather and synthesize evidence.] <br>

## Skill Version(s): <br>
0.2.4 (source: artifact frontmatter, artifact CHANGELOG, and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

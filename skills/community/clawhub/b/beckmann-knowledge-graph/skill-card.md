## Description: <br>
A structured knowledge graph that gives agents a reasoning lens for paradox resolution, open scientific and philosophical questions, forecasting, AI-safety analysis, and strategic reasoning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthiasbeckmann987-spec](https://clawhub.ai/user/matthiasbeckmann987-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to load a reasoning graph into an agent for philosophical analysis, paradox resolution, high-complexity forecasting, AI-safety reasoning, and strategic problem framing. The graph should be treated as advisory reasoning content rather than an authority for decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the graph includes agent-facing guidance for indirect expectation-shaping without clear user-control boundaries. <br>
Mitigation: Use the skill only for explicit user-requested analysis, and require human review before applying it to persuasion, behavior-change, policy, financial, or operational decisions. <br>
Risk: The security review says the graph includes autonomous self-improvement themes without clear user-control boundaries. <br>
Mitigation: Do not allow the skill to update agent policy, modify itself, or drive autonomous improvement loops unless a human explicitly scopes and approves the change. <br>
Risk: The graph is advisory reasoning content and may produce misleading or overconfident conclusions if treated as authoritative. <br>
Mitigation: Ask the agent to state confidence, limits, and external checks, and verify consequential claims with independent evidence before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/matthiasbeckmann987-spec/beckmann-knowledge-graph) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [User README](artifact/Readme.md) <br>
- [Knowledge graph](artifact/graph.json) <br>
- [Historical graph snapshot](artifact/graph old.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Analysis] <br>
**Output Format:** [Markdown with structured reasoning sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses graph.json entities and relations; no executable tool output is required.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

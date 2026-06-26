## Description: <br>
Automatically extracts entities, events, and causal relationships from logs and memory files to build a dynamic knowledge graph for querying and visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weidadong2359](https://clawhub.ai/user/weidadong2359) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to scan OpenClaw memory files, derive entities, dated events, and causal links, and produce a local graph for analysis or visualization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The graph can preserve sensitive names, projects, incidents, and relationships from OpenClaw memory files. <br>
Mitigation: Review and redact memory files before running the skill, and restrict access to the generated memory/causal-graph.json file. <br>
Risk: Future LLM-based extraction could send private memory content to an external provider. <br>
Mitigation: Use only approved providers and redact sensitive content before enabling any LLM extraction path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weidadong2359/causal-graph) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Console text summary and local JSON graph file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes memory/causal-graph.json in the configured OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

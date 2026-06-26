## Description: <br>
Generates standalone interactive HTML node-graph diagrams for code architecture, module relationships, function call chains, data flows, and UI layout hierarchies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biubiubiu533](https://clawhub.ai/user/biubiubiu533) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to quickly map a project into browsable architecture, call-chain, data-flow, and UI hierarchy diagrams for code comprehension and documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads project source files to infer architecture and call flows, so generated diagrams may expose sensitive implementation details. <br>
Mitigation: Review generated diagrams before sharing, committing, or publishing them. <br>
Risk: The artifact includes broad cleanup behavior that could remove files beyond the intended diagram outputs. <br>
Mitigation: Before use, instruct the agent to delete only files it created in docs/code_graph and to preserve all other project files. <br>


## Reference(s): <br>
- [Code Flow Graph Data Format Reference](references/data_format.md) <br>
- [Code Flow Graph README](README.md) <br>
- [ClawHub release page](https://clawhub.ai/biubiubiu533/code-flow-graph) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, configuration, guidance] <br>
**Output Format:** [Standalone HTML viewer plus JavaScript diagram data files, with explanatory agent guidance during generation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates code_flow_graph.html and code_flow_graph_data.js, usually under docs/code_graph, and may append additional diagram pages after user-selected deep dives.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

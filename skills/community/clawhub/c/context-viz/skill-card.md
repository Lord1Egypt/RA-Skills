## Description: <br>
Visualize the current context window usage - token estimates per component (system prompt, tools, workspace files, messages, free space). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[furukama](https://clawhub.ai/user/furukama) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to inspect current context usage, estimate token consumption by workspace files and messages, and see remaining context capacity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled helper reads standard context files and the memory/ directory from the workspace selected by the user. <br>
Mitigation: Run it only against the intended workspace and avoid unrelated or highly sensitive directories. <br>
Risk: Token totals are approximate and may not exactly match model tokenization. <br>
Mitigation: Use the visualization as an operational estimate and rely on session-reported context totals when exact capacity matters. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with monospace text charts and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Token counts are estimates based on local workspace files and session context status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

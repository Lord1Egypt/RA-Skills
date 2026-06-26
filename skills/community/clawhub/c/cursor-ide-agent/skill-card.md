## Description: <br>
Use Cursor Agent for coding tasks through either the local Cursor CLI or a connected VS Code/Cursor IDE node, choosing the CLI for fast repository work and the IDE node path for diagnostics, references, debugging, tests, and other editor-aware workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoyaner0201](https://clawhub.ai/user/xiaoyaner0201) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to delegate coding, review, refactoring, debugging, testing, and git workflows to Cursor Agent from a terminal or from a connected VS Code/Cursor workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cursor Agent workflows can modify repositories, run commands, and commit changes with broad autonomy when used in agent or force modes. <br>
Mitigation: Start in ask or plan mode for unfamiliar repositories, work on a branch, review repository instruction files, inspect diffs before committing, and avoid force mode unless unattended edits are intended. <br>
Risk: Background runs, sandbox disabling, and cloud handoff can increase unattended execution authority and data-sharing exposure. <br>
Mitigation: Keep sandboxing enabled when possible, use trusted installation and node connections, review MCP configuration, and use background or cloud execution only when that level of authority and sharing is acceptable. <br>


## Reference(s): <br>
- [Cursor CLI install](https://cursor.com/install) <br>
- [Cursor Agents](https://cursor.com/agents) <br>
- [OpenClaw Node for VS Code extension](https://marketplace.visualstudio.com/items?itemName=xiaoyaner.openclaw-node-vscode) <br>
- [vscode-node companion skill](https://clawhub.ai/xiaoyaner0201/vscode-node) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON command parameters, and workflow tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires either the Cursor Agent CLI binary or a connected OpenClaw Node for VS Code/Cursor workspace.] <br>

## Skill Version(s): <br>
3.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

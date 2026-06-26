## Description: <br>
SOP for terminal-based, git-native AI pair programming with Aider, covering git work trees, tree-sitter repo maps, edit formats, human-in-the-loop REPL workflows, architect/editor mode, and auto-test loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentsope](https://clawhub.ai/user/agentsope) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coder-agents use this skill to operate Aider in existing git repositories, scope edits to small file sets, choose model-appropriate edit formats, run architect/editor workflows, and validate changes while preserving reviewable commits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill recommends terminal and git workflows that can modify a working tree when followed by an agent or engineer. <br>
Mitigation: Review proposed commands before execution and start from a clean or intentionally saved git state. <br>
Risk: Aider sessions may expose repository contents or secrets to the selected model provider if sensitive files are added to context. <br>
Mitigation: Avoid adding secrets or unrelated sensitive files to the Aider session and review context before using paid or external model services. <br>


## Reference(s): <br>
- [Aider GitHub Repository](https://github.com/Aider-AI/aider) <br>
- [Aider Architecture Reference](references/R1-architecture.md) <br>
- [Aider SOP Workflow Reference](references/R2-sop-workflow.md) <br>
- [Aider Dilemma Cases Reference](references/R3-dilemma-cases.md) <br>
- [Aider Anti-Patterns Reference](references/R4-anti-patterns.md) <br>
- [Aider Ecosystem Context Reference](references/R5-ecosystem-context.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and decision tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for an agent or engineer; it does not directly execute commands.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

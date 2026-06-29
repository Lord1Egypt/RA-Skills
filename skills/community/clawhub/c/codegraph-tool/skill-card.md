## Description: <br>
CodeGraph is a pre-indexed code knowledge graph tool that provides semantic code intelligence for Claude Code, Cursor, Codex, Gemini, OpenCode, Hermes, Antigravity, Kiro, and other AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install and operate CodeGraph for local code indexing, semantic code exploration, symbol search, call-chain tracing, and change-impact analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents a curl-to-sh installation path that executes a remote shell script. <br>
Mitigation: Prefer the npx or npm installation path and review the remote installer before using it. <br>
Risk: CodeGraph creates a local code index that may include repository structure and source context. <br>
Mitigation: Initialize it only in repositories you are comfortable indexing and review exclusions such as .gitignore before use. <br>
Risk: Optional auto-allow settings can let an agent query the CodeGraph MCP index without repeated prompts. <br>
Mitigation: Avoid auto-allow settings unless the user is comfortable with that access pattern. <br>


## Reference(s): <br>
- [ClawHub Codegraph Tool release](https://clawhub.ai/openlark/codegraph-tool) <br>
- [CodeGraph Configuration & Reference](references/configuration.md) <br>
- [CodeGraph Architecture](references/architecture.md) <br>
- [CodeGraph install script](https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, configuration snippets, and tool guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP tool names, CLI commands, and JSON-oriented query options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

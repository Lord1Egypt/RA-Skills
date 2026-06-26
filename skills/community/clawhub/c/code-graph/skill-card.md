## Description: <br>
Installs GitNexus, configures MCP integration, and indexes the current project into a code knowledge graph. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[babywhale](https://clawhub.ai/user/babywhale) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to install GitNexus, configure MCP access for supported editors, and create or refresh a project code graph for search, context, impact analysis, and refactoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can install GitNexus globally or run it through npx and can update editor/MCP configuration. <br>
Mitigation: Review npm/npx commands before execution and run the setup only when you want GitNexus installed and configured. <br>
Risk: Troubleshooting guidance includes a git add/commit example that may stage unintended files. <br>
Mitigation: Review .gitignore and staged files before running any git add or commit commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/babywhale/code-graph) <br>
- [Node.js](https://nodejs.org/) <br>
- [nvm](https://github.com/nvm-sh/nvm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides idempotent setup checks before installation, MCP configuration, indexing, and verification.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

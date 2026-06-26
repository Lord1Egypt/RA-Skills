## Description: <br>
Structured memory system for AI agents with checkpoint and recovery workflows, typed Markdown storage, Obsidian-compatible templates, and local search support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[azrijamil](https://clawhub.ai/user/azrijamil) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to preserve working context across sessions by creating structured memory vault entries, checkpoints, handoffs, and searchable knowledge records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The memory vault may contain sensitive project context, personal details, or operational notes. <br>
Mitigation: Use a workspace-specific vault for sensitive work, avoid storing secrets or regulated personal data, and keep vaults and .env files out of public repositories or broad sync folders. <br>
Risk: Bulk migration commands can modify an existing Markdown knowledge base. <br>
Mitigation: Run migrations with --dry-run first and use a verified backup before modifying an existing vault. <br>
Risk: The CLI is installed from an npm package controlled by a third-party publisher. <br>
Mitigation: Install only when the npm package publisher is trusted and review package provenance according to local supply-chain policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/azrijamil/fsxmemory) <br>
- [npm package: @foresigxt/foresigxt-cli-memory](https://www.npmjs.com/package/@foresigxt/foresigxt-cli-memory) <br>
- [qmd search dependency](https://github.com/tobi/qmd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and structured memory templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce or modify local Markdown vault files when the documented fsxmemory commands are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

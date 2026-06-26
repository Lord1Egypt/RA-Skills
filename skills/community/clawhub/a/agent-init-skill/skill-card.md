## Description: <br>
Initialize or update AGENTS.md/CLAUDE.md for a project. Use this skill whenever the user wants to create, initialize, generate, setup, or update a project-level AGENTS.md or CLAUDE.md file. Triggers on requests like "initialize AGENTS.md", "create CLAUDE.md", "generate project doc for AI", "setup agent guidelines", "create project rules", or any mention of AGENTS.md/CLAUDE.md creation or initialization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[orbisz](https://clawhub.ai/user/orbisz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create or update project-level AGENTS.md or CLAUDE.md guidance for AI coding tools. It analyzes project structure, commands, conventions, and documentation needs, then organizes them into a reusable Markdown template. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect repositories and rewrite project-level AI instruction files. <br>
Mitigation: Require explicit approval before file writes and review AGENTS.md or CLAUDE.md diffs before committing them. <br>
Risk: The artifact includes a self-evolution section that could encourage persistent changes outside the requested documentation task. <br>
Mitigation: Remove or ignore the self-evolution section before use. <br>
Risk: Generated project guidance can include incorrect commands, file paths, or conventions if repository inspection is incomplete. <br>
Mitigation: Verify generated commands, referenced paths, and documented conventions against the repository before relying on the file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/orbisz/agent-init-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown project instruction file with tables, checklists, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes or updates AGENTS.md or CLAUDE.md in the project root.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

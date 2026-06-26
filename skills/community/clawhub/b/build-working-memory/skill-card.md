## Description: <br>
Set up, migrate, and manage a file-based working memory system that helps AI agents preserve session continuity, retrieve project context, and maintain dated memory records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiyuan](https://clawhub.ai/user/jiyuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to scaffold or migrate project-local working memory, load relevant context at session start, and persist daily logs, threads, state, and structured dated events across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates persistent project-local memory files that may retain sensitive details if users store secrets, credentials, or personal information. <br>
Mitigation: Avoid storing secrets, credentials, and sensitive personal details in memory files; review memory content during curation. <br>
Risk: Migration can modify AGENT.md or AGENTS.md by appending standing memory-management instructions. <br>
Mitigation: Run migration with --dry-run first, review the resulting agent-instruction diffs, or use --skip-agent-patch when instruction changes are not wanted. <br>


## Reference(s): <br>
- [Migration Reference](references/MIGRATION.md) <br>
- [Retrieval Workflow](references/RETRIEVAL.md) <br>
- [Schema Reference](references/SCHEMAS.md) <br>
- [Structured Events and Temporal Support](references/TEMPORAL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and shell commands; generated memory artifacts use Markdown and JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates project-local memory files and can append working-memory instructions to AGENT.md or AGENTS.md during migration.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

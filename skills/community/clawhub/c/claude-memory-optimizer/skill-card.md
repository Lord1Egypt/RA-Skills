## Description: <br>
Structured memory system with 4-type classification (user/feedback/project/reference), frontmatter metadata, and automated migration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mystour](https://clawhub.ai/user/mystour) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to organize long-term memory into user, feedback, project, and reference categories, add frontmatter metadata, and migrate existing flat memory files into a structured layout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can bulk rewrite, move, and reindex memory files without enough warning or rollback detail. <br>
Mitigation: Back up the memory directory before migration, prefer preview or dry-run behavior where available, confirm exactly which files will change, and avoid running it on a primary memory store until rollback steps are clear. <br>


## Reference(s): <br>
- [README.md](README.md) <br>
- [MEMORY-OPTIMIZATION.md](MEMORY-OPTIMIZATION.md) <br>
- [ClawHub skill page](https://clawhub.ai/mystour/claude-memory-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and generated memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or execute file migration commands that rewrite, move, and reindex memory files.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and package.json; SKILL.md frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

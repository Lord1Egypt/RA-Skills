## Description: <br>
Organize project documentation by size, audience, and freshness for new documentation setup, restructuring, slimming bloated CLAUDE.md or AGENTS.md files, deciding where docs should live, and documentation best-practice questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zning1994](https://clawhub.ai/user/zning1994) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, maintainers, and AI coding-agent users use this skill to choose documentation structure, classify existing docs by audience and freshness, slim oversized agent instruction files, reduce duplicated facts, and plan safe documentation migrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation reorganization proposals may include moving or deleting files such as logs, media, chat exports, or duplicated documentation. <br>
Mitigation: Work on a branch or snapshot and review proposed moves or deletions before letting an agent apply them. <br>
Risk: Path changes can break implicit references in CI, docker-compose files, Makefiles, scripts, or ignore files. <br>
Mitigation: Search for filename references before moving files and update all affected paths as part of the migration. <br>


## Reference(s): <br>
- [Docs Organization ClawHub page](https://clawhub.ai/zning1994/docs-organization) <br>
- [Docs Organization source homepage](https://github.com/zning1994/docs-organization) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with directory templates, checklists, metadata examples, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable artifact is produced; recommended file moves and deletions require user review.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and changelog, released 2026-04-08) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Creates command-style automation skills for Claude Code projects, especially slash commands for repeatable workflows such as deploys, commits, releases, migrations, scaffolding, and cross-repo operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn repeatable Claude Code workflows into command-style skills under `.claude/skills/`. It is most relevant when the workflow may include side effects such as deploys, commits, migrations, file changes, external API calls, or cross-repo updates that need approval gates and verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated command skills can encode side-effecting workflows such as commits, deploys, cross-repo edits, or external API calls. <br>
Mitigation: Review each generated command before enabling it and require explicit approval gates before irreversible actions. <br>
Risk: A generated command could provide incorrect or misleading automation guidance if the target workflow or project conventions are misunderstood. <br>
Mitigation: Read the target project's conventions, verify generated commands against the workflow, and scan the skill before deployment. <br>


## Reference(s): <br>
- [Command Skill Design Patterns](references/design-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/tenequm/command-skill-creator) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown skill files with YAML frontmatter, phased workflow instructions, approval gates, audit checklists, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated command skills should be reviewed before use, especially when they can commit, deploy, modify another repository, or call external APIs.] <br>

## Skill Version(s): <br>
0.1.1 (source: SKILL.md metadata and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

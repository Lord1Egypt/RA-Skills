## Description: <br>
Generates repository-facing AI guidance, including AGENTS.md and supporting coding style and architecture documentation, so coding agents can understand, build, test, and navigate a project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linuxcer](https://clawhub.ai/user/linuxcer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to create or refresh AI-facing project guidance for repositories, including AGENTS.md, coding-style notes, architecture notes, and documentation navigation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can replace CLAUDE.md with a symlink to AGENTS.md, which may overwrite existing repository-specific agent instructions. <br>
Mitigation: Check whether CLAUDE.md already exists and require a reviewed diff or explicit confirmation before allowing symlink creation or file updates. <br>
Risk: The skill reads representative source files and edits repository documentation, which can introduce inaccurate guidance if run without review. <br>
Mitigation: Run it only on intended repositories and review generated or merged documentation before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linuxcer/agentsmd-creator) <br>
- [Community coding standards](artifact/references/community-standards.md) <br>
- [AGENTS.md template](artifact/references/template.md) <br>
- [Programming principles](artifact/references/principles.md) <br>
- [Programming principle examples](artifact/references/examples.md) <br>
- [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown files and concise status text with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets AGENTS.md under 200 lines and may create or update docs/CODING_STYLE.md, docs/ARCHITECTURE.md, and a CLAUDE.md symlink.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

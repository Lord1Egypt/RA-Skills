## Description: <br>
Builds a runnable Claude Code Agent Teams skill package that produces SKILL.md as a lead-operator playbook, agents/<role>.md subagent definitions for runtime spawning, references/<role>.md role specs with 8 sections, and optional hooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering leads use this skill to create reusable multi-agent team packages for Claude Code, including lead playbooks, role definitions, role specifications, and optional quality hooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated agent definitions can grant broad tool access or file-editing authority if role allowlists are too permissive. <br>
Mitigation: Review every generated agents/<role>.md file and keep tool allowlists narrow before installing the team. <br>
Risk: User-wide installation of generated agents can make them available outside the intended project. <br>
Mitigation: Prefer project-scoped .claude/agents installation unless reuse across projects is intentional. <br>
Risk: Optional hook scripts can block or alter workflow behavior when enabled. <br>
Mitigation: Inspect hook scripts before enabling them and scope them to the intended project. <br>
Risk: Agent Teams runtime sessions can remain active after the work is finished. <br>
Mitigation: Run the documented teardown steps when the generated team is finished. <br>


## Reference(s): <br>
- [create-team on ClawHub](https://clawhub.ai/xiejinsong/create-team) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Templates](artifact/references/templates.md) <br>
- [Validation checklist](artifact/references/checklist.md) <br>
- [Claude Code sub-agents documentation](https://code.claude.com/docs/en/sub-agents) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files with inline code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a structured skill package with SKILL.md, agents/<role>.md, references/<role>.md, and optional hooks/ artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

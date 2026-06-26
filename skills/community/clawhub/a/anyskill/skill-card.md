## Description: <br>
AnySkill manages, syncs, dynamically loads, uploads, shares, and batch installs agent skills from a GitHub-backed repository for OpenClaw, Antigravity, Claude Code, and Cursor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyijianke](https://clawhub.ai/user/lanyijianke) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use AnySkill to connect a private GitHub skill repository, load matching skills on demand, and synchronize skill files across supported IDEs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles write-capable GitHub tokens for private skill repositories. <br>
Mitigation: Use a fine-grained token limited to one repository and store it in a secure environment or platform secret store instead of pasting it into chat or plaintext configuration. <br>
Risk: The skill can persistently change agent or workspace behavior through skill downloads, workspace configuration updates, infrastructure changes, commits, pushes, or delete workflows. <br>
Mitigation: Review any TOOLS.md, AGENTS.md, downloaded skill, infrastructure update, commit, push, or delete action before allowing it. <br>


## Reference(s): <br>
- [AnySkill homepage](https://github.com/lanyijianke/AnySkill) <br>
- [ClawHub skill page](https://clawhub.ai/lanyijianke/anyskill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local skill files, configuration files, and Git commits during repository management workflows.] <br>

## Skill Version(s): <br>
1.0.7 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

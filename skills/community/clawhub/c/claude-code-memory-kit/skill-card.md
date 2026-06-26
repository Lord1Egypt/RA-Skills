## Description: <br>
Stop Claude Code from repeating mistakes by enforcing guardrails, preserving context, and maintaining consistency across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhinas90](https://clawhub.ai/user/abhinas90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams using Claude Code use this skill as a pattern guide for project memory files, recurring mistake tracking, and optional command guardrails across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project memory files may accidentally capture secrets, tokens, private database credentials, or sensitive customer data. <br>
Mitigation: Review CLAUDE.md, memory.md, mistakes.md, and bootstrap.md before use and keep secrets or sensitive customer data out of these files. <br>
Risk: Optional Claude Code settings changes can affect confirmation behavior for high-risk commands. <br>
Mitigation: Review the optional settings changes before enabling them and test guardrails with non-destructive commands first. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/abhinas90/claude-code-memory-kit) <br>
- [Installation Guide](artifact/INSTALL.md) <br>
- [Troubleshooting Guide](artifact/TROUBLESHOOTING.md) <br>
- [Claude Code Rules Template](artifact/templates/CLAUDE.md) <br>
- [Session Bootstrap Template](artifact/templates/bootstrap.md) <br>
- [Project Memory Template](artifact/templates/memory.md) <br>
- [Mistakes Template](artifact/templates/mistakes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Guidance, Shell commands] <br>
**Output Format:** [Markdown templates with inline shell and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Template-based guidance with no executable payload or hidden automation, according to server security evidence.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

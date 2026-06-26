## Description: <br>
Say 'sync my agent configs' to write coding rules once and sync to Claude Code, Cursor, Copilot, Windsurf, and 4 more agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[singggggyee](https://clawhub.ai/user/singggggyee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to maintain shared agent rules in one RULES.md file, check configuration drift, convert between agent config formats, and synchronize rules across supported coding agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configuration sync can propagate incorrect or overly broad rules across multiple coding agents. <br>
Mitigation: Review the generated diffs before writing changes and keep agent-specific sections that should not be overwritten. <br>
Risk: The skill is intended for development or maintainer contexts where the agent may inspect repository files and use project tooling. <br>
Mitigation: Install it only in trusted workspaces and use normal sandbox prompts when you do not want broad command execution. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/SingggggYee/dotpilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance, diffs, and agent configuration file content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or update RULES.md and supported agent configuration files after showing diffs.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata; SKILL.md frontmatter lists 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

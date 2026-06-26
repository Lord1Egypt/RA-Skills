## Description: <br>
Production skill for orchestrating Claude Code's native agent teams feature for multi-lens reviews, competing-hypotheses debugging, full-stack features, architecture debates, and cross-domain investigations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthew-a-gordon](https://clawhub.ai/user/matthew-a-gordon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to coordinate Claude Code agent teams for parallel code reviews, debugging, feature work, architecture decisions, performance investigations, and bulk classification or refactoring tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Parallel Claude Code agents can create conflicting or unsafe edits when work boundaries are unclear. <br>
Mitigation: Assign narrow file or directory ownership, review all diffs and generated files, and run tests before merging. <br>
Risk: Prompts or team messages can expose secrets or sensitive project data to agent sessions. <br>
Mitigation: Avoid putting secrets in prompts and keep agent work scoped to the minimum project files needed. <br>
Risk: Force cleanup can interrupt active Claude Code sessions before work is saved or reviewed. <br>
Mitigation: Use graceful cleanup by default and use force cleanup only when no important Claude Code session is running. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/matthew-a-gordon/claude-code-teams) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>
- [Claude Code repository](https://github.com/anthropics/claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with copy-paste prompts and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces team templates, setup guidance, monitoring commands, cleanup commands, and review or implementation plans for Claude Code agent teams.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Auto Skill Loader detects a task's intent, matches an appropriate installed skill, and can load or route work while respecting core, protected, and dynamic skill levels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zqleslie](https://clawhub.ai/user/zqleslie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to help an agent discover installed OpenClaw skills, select a relevant skill for a user request, preview matches, and optionally route work to another agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically choose and load other installed skills, which gives it broad influence over which instructions handle a user request. <br>
Mitigation: Install it only when automatic skill selection is intended, review available workspace and global skills first, and use dryRun or strict matching for higher-control environments. <br>
Risk: Optional agent routing can delegate work to another agent when enabled. <br>
Mitigation: Disable routing unless delegation is needed, and avoid using the skill with untrusted local skills or agents. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/zqleslie/auto-skill-loader) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with optional shell commands, YAML configuration, and JSON output from the helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run in dry-run mode to preview matching behavior before loading a skill.] <br>

## Skill Version(s): <br>
2.0.1 (source: SKILL.md frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

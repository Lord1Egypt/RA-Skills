## Description: <br>
Checks local Baiyin skills under the skill/ directory against SkillHub, upgrades eligible skills with backup and rollback, and then resumes the original task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiuping520](https://clawhub.ai/user/jiuping520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams using Baiyin skills use this skill to check installed Baiyin skill directories against SkillHub, upgrade one or more skills when newer versions are available, and continue the original workflow after the update step. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can replace local Baiyin skill files with versions fetched from SkillHub, which may change future agent behavior. <br>
Mitigation: Install and run it only when the Baiyin SkillHub source is trusted, and review update summaries before relying on changed skills. <br>
Risk: Automatic upgrades can apply remote changes without a fresh prompt once enabled. <br>
Mitigation: Keep version control or backups for skill directories and enable automatic upgrades only in environments where unattended skill changes are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiuping520/baiyin-skills-upgrade) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status summaries with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local Baiyin skill files, write backups, restore from rollback, and record upgrade state within the relevant skill directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Alvis GitHub CLI helps agents use the GitHub CLI (gh) for authenticated repository, issue, pull request, release, and basic repository management operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and repository maintainers use this skill to ask an agent to prepare or run GitHub CLI workflows for authentication checks, repository management, issues, pull requests, and releases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated GitHub CLI commands can act with the user's GitHub credentials and affect repositories. <br>
Mitigation: Use the skill only in trusted maintainer environments, verify authentication and repository targets before writes, and review commands before execution. <br>
Risk: Repository-changing workflows such as pull request merges, releases, or destructive maintenance can affect the wrong project if the target is unclear. <br>
Mitigation: Confirm the owner, repository, branch, and action before running write operations, and prefer explicit command flags over interactive prompts. <br>


## Reference(s): <br>
- [Complete setup guide](https://SkillBoss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include repository URLs, command outputs, and confirmation prompts for user review.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

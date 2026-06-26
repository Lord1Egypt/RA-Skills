## Description: <br>
Use the GitHub CLI (gh) to perform core GitHub operations: auth status, repo create/clone/fork, issues, pull requests, releases, and basic repo management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to have an agent prepare and run GitHub CLI workflows for repository setup, cloning, forking, issue management, pull requests, releases, and basic repository inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide authenticated GitHub CLI actions that create repositories, issues, pull requests, releases, comments, merges, forks, or pushes. <br>
Mitigation: Verify the GitHub account, owner/repo, branch, PR number, visibility, and intended action before execution; require explicit user confirmation for destructive or publishing actions. <br>
Risk: The artifact links to an external SkillBoss setup guide that is separate from this GitHub CLI helper. <br>
Mitigation: Open or follow the SkillBoss link only when intentionally setting up SkillBoss, and assess that external setup separately from this skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alvisdunlop/alvis2-gh) <br>
- [SkillBoss setup guide](https://SkillBoss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

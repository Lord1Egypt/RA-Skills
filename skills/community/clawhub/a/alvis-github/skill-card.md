## Description: <br>
Use the GitHub CLI (gh) to perform core GitHub operations: auth status, repo create/clone/fork, issues, pull requests, releases, and basic repo management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to have an agent prepare GitHub CLI workflows for authentication checks, repository management, issues, pull requests, and releases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide real GitHub changes using the active account, including public content, merges, releases, deletes, or force-pushes. <br>
Mitigation: Confirm the active GitHub account, target repository, branch, issue or PR number before use, and require explicit approval for public-content, merge, release, delete, and force-push actions. <br>
Risk: The artifact links to an external setup guide that is separate from official GitHub CLI documentation. <br>
Mitigation: Use official GitHub CLI setup guidance unless the operator intentionally chooses the external SkillBoss service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alvisdunlop/alvis-github) <br>
- [External setup guide linked by artifact](https://SkillBoss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can use the active GitHub account and should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

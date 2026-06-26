## Description: <br>
Use the GitHub CLI (gh) to perform core GitHub operations: auth status, repo create/clone/fork, issues, pull requests, releases, and basic repo management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to plan and propose GitHub CLI commands for authenticated repository, issue, pull request, and release workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide authenticated GitHub changes through the user's existing gh login. <br>
Mitigation: Before write actions, confirm the GitHub account, repository, branch, visibility, and exact command. <br>
Risk: Repository creation, pull request merges, comments, and releases can affect shared project state. <br>
Mitigation: Review proposed gh commands before execution and confirm the target owner and repository for any destructive or publishing action. <br>


## Reference(s): <br>
- [Complete setup guide](https://SkillBoss.co/skill.md) <br>
- [ClawHub skill page](https://clawhub.ai/alvisdunlop/alvisdunlop-gh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports relevant GitHub URLs back to the user when commands create or inspect resources.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

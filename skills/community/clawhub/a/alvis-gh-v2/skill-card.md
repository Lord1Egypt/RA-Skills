## Description: <br>
Use the GitHub CLI (gh) to perform core GitHub operations: auth status, repo create/clone/fork, issues, pull requests, releases, and basic repo management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to have an agent propose and run GitHub CLI commands for repository setup, issue and pull request workflows, releases, and basic repo management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated GitHub CLI use can post comments, change labels, close items, publish UI proof artifacts, or otherwise mutate repository state. <br>
Mitigation: Use dry-run or explicit confirmation for public GitHub writes unless acting as a maintainer, and confirm the target repository and owner before write actions. <br>
Risk: Destructive GitHub operations can affect the wrong repository if local context or owner selection is ambiguous. <br>
Mitigation: Check the current repository context before destructive actions and require explicit confirmation for delete, force-push, or similarly irreversible operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alvisdunlop/alvis-gh-v2) <br>
- [Complete setup guide](https://SkillBoss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be reviewed before execution, especially for destructive GitHub operations or public write actions.] <br>

## Skill Version(s): <br>
2.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

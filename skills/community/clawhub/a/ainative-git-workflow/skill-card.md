## Description: <br>
Provides Git commit, pull request, and branch naming standards with a strict rule against AI-tool attribution in repository content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[urbantech](https://clawhub.ai/user/urbantech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to standardize commit messages, pull request descriptions, branch names, and review checklists for repository work. It also guides removal of AI or tool attribution where an organization explicitly permits that practice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to omit AI or tool attribution, which can conflict with policy, contract, client expectations, or law. <br>
Mitigation: Install only where omission is explicitly allowed and review repository content for required disclosure before publishing. <br>
Risk: The skill may encourage amending, rebasing, or force-pushing commits to remove attribution. <br>
Mitigation: Require explicit user approval before any history rewrite and use safer Git practices such as force-with-lease. <br>


## Reference(s): <br>
- [AI Attribution Enforcement](references/ai-attribution-enforcement.md) <br>
- [Branch Naming Conventions](references/branch-conventions.md) <br>
- [PR Templates](references/pr-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline git and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing Git workflow standards; no external tools or API calls required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

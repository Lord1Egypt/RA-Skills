## Description: <br>
Provides expert guidance for branching strategies, commit standards, code review workflows, monorepo management, release automation, and repository health practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to assess repository health and generate practical Git workflow guidance, including branch strategy, pull request standards, branch protection, release automation, monorepo structure, and recovery playbooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Git commands can affect repository history or configuration, including rebases, resets, filter-repo cleanup, force pushes, global Git config, hooks, and branch protection changes. <br>
Mitigation: Before applying commands to an important repository, confirm the target repository and branch, review the exact command, back up or test on a disposable clone when appropriate, and make sure the team agrees with the workflow. <br>
Risk: The skill provides workflow guidance and templates, so recommendations may not match a team's existing compliance, release, or access-control requirements. <br>
Mitigation: Treat generated workflow changes as proposals, review them with repository owners, and adapt branch protection, CI, CODEOWNERS, signing, and release settings to the team's policies before rollout. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1kalin/afrexai-git-engineering) <br>
- [Publisher profile](https://clawhub.ai/user/1kalin) <br>
- [AfrexAI Context Packs](https://afrexai-cto.github.io/context-packs/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, YAML snippets, templates, checklists, and decision matrices.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are advisory and may include repository-specific commands or configuration examples that should be reviewed before applying.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

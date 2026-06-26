## Description: <br>
Publishes local changes to a GitHub pull request, monitors review feedback and required checks, and helps address issues until the PR is ready. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patrick-erichsen-2](https://clawhub.ai/user/patrick-erichsen-2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to prepare and publish local changes as a GitHub PR, then iterate on review comments and failing required checks while preserving user approval gates for high-impact actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authorized runs can commit, push, open pull requests, and modify code while addressing review or CI feedback. <br>
Mitigation: Confirm the target repository, branch, and PR before use; review pre-publish findings and approve publishing or fix actions explicitly. <br>
Risk: Review or CI fixes can be incorrect, incomplete, or conflict with product intent. <br>
Mitigation: Review proposed changes and local validation results before relying on the PR, and pause for user judgment on ambiguous or scope-expanding requests. <br>
Risk: Some CI failures may require secrets, paid services, release credentials, or remote-only infrastructure. <br>
Mitigation: Treat those cases as blockers and require explicit user direction before using elevated or remote workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/patrick-erichsen-2/all-green) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown status updates, review findings, command plans, and code or configuration changes as needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May commit, push, open pull requests, and modify code only within the user-approved PR workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

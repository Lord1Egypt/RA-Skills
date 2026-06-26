## Description: <br>
Audit GitHub/GitLab branch protection rules across repositories, identify gaps in reviews, status checks, force-push restrictions, admin bypass, and CODEOWNERS enforcement, and generate recommended rulesets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and compliance teams use this skill to audit branch protection posture across GitHub or GitLab repositories and produce remediation recommendations before security or compliance reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The fix workflow can directly change GitHub branch protection settings. <br>
Mitigation: Confirm the owner, repository, and branch before applying changes; review required status checks and review rules; use a least-privileged GitHub token; prefer dry-run or manual application for production repositories. <br>


## Reference(s): <br>
- [Branch Protection Auditor on ClawHub](https://clawhub.ai/charlie-morrison/branch-protection-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and branch protection configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include repository audit tables, recommended rulesets, compliance mappings, and GitHub CLI commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

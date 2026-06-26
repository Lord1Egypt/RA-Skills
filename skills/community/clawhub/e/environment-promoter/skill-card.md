## Description: <br>
Manage environment promotions between development, staging, and production by comparing configuration, detecting drift, generating promotion plans, validating prerequisites, and preparing rollback guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, release engineers, and operations teams use this skill to inspect environment differences, identify configuration drift, plan promotions, validate readiness, and document rollback steps before deployment changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Environment comparisons can expose secrets or sensitive deployment values from environment and configuration files. <br>
Mitigation: Use key-only or hash-only comparisons by default, mask sensitive values, and manually review generated diffs before sharing them. <br>
Risk: Validation and history commands may run live checks using local credentials, configured URLs, or GitHub CLI access. <br>
Mitigation: Run the skill only in authorized repositories and require explicit confirmation before curl-based validation or GitHub CLI history commands. <br>


## Reference(s): <br>
- [Environment Promoter on ClawHub](https://clawhub.ai/charlie-morrison/environment-promoter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Human-readable text, Markdown reports, JSON summaries, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Masks some sensitive values in examples, but generated diffs and checks still require human review before sharing or execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

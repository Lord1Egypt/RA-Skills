## Description: <br>
Perform 12-Factor App compliance analysis on codebases for application architecture evaluation, SaaS audits, and cloud-native reviews against the original 12-Factor methodology. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, architects, and reviewers use this skill to evaluate a repository against the Twelve-Factor App methodology and identify gaps in SaaS, cloud-native, or containerization readiness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository analysis can surface sensitive configuration details, including secret names, API key patterns, database URLs, or file paths in generated findings. <br>
Mitigation: Run the skill only against repositories intended for review and redact sensitive findings before sharing reports outside the review team. <br>
Risk: Automated compliance classifications may be incomplete or misleading if repository structure, generated files, or framework conventions are not fully interpreted. <br>
Mitigation: Treat the report as review guidance and verify findings against the codebase before making architecture, deployment, or compliance decisions. <br>


## Reference(s): <br>
- [The Twelve-Factor App](https://12factor.net) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with an executive summary table, per-factor findings, evidence, gaps, and recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a target codebase path and local repository inspection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

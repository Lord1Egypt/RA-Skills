## Description: <br>
Smart dependency health check for security audits, outdated package detection, unused dependency review, and prioritized update planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Fratua](https://clawhub.ai/user/Fratua) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to review project dependencies across common package ecosystems, identify security, freshness, and unused dependency issues, and prepare a prioritized remediation plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated audit, install, or fix commands may change dependencies or install helper tools. <br>
Mitigation: Review commands before execution, run from a clean working tree, avoid sudo, and test dependency changes before merging. <br>
Risk: Networked audit commands may send dependency metadata to package registries or external audit services. <br>
Mitigation: Confirm registry, privacy, and private dependency requirements before running audits against proprietary projects. <br>


## Reference(s): <br>
- [Dependency Audit on ClawHub](https://clawhub.ai/Fratua/dependency-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes prioritized findings, safe update commands, and dependency health summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

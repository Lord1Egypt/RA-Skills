## Description: <br>
Audits project dependencies across npm, pip, cargo, Go, Composer, and related ecosystems for outdated, vulnerable, unused, and license-incompatible packages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit project dependencies, prioritize security and freshness updates, identify unused packages, and flag license compatibility issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency audit and remediation commands may install tools, access package registries, or modify project dependencies. <br>
Mitigation: Require explicit approval before package installs, npx tools, npm audit fix, pip-audit --fix, or dependency removals; prefer a branch, virtual environment, or container for scans that may touch the network or local tooling. <br>
Risk: Upgrade recommendations can introduce breaking changes when major updates or force-fix commands are applied without review. <br>
Mitigation: Review changelogs for major upgrades, prioritize critical fixes, batch lower-risk patch updates, and run the project test suite after each upgrade batch. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/dependency-health-check) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prioritized dependency health report covering outdated packages, vulnerabilities, unused dependencies, license flags, and upgrade sequencing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

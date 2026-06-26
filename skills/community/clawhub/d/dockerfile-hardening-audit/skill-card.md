## Description: <br>
Statically audit Dockerfiles for common container hardening risks (root user, unpinned/latest base images, missing healthchecks, and risky build patterns). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to scan Dockerfiles before production release, rank hardening risks, and optionally fail builds when critical container configuration issues are found. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit reports can reveal private repository structure through Dockerfile paths and flagged lines. <br>
Mitigation: Treat generated reports as internal review material and avoid publishing them when paths or findings disclose sensitive project details. <br>
Risk: Static Dockerfile checks may miss context-specific container risks or produce findings that need engineering judgment. <br>
Mitigation: Use the report as a review aid, tune the glob and regex filters for the target repository, and manually review critical findings before release decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/dockerfile-hardening-audit) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Text, JSON, Shell commands] <br>
**Output Format:** [Plain text report or structured JSON audit output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can exit with status 1 when FAIL_ON_CRITICAL=1 and one or more Dockerfiles are classified as critical.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

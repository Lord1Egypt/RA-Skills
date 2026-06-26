## Description: <br>
Analyze the blast radius of upgrading, removing, or replacing a dependency by tracing imports, finding affected files, checking test coverage of impacted code, detecting breaking API changes, and generating upgrade plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill before dependency upgrades, removals, or replacements to understand affected files, likely breakage, test coverage gaps, and migration work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects files in the current repository and may reveal dependency usage patterns or source paths in its output. <br>
Mitigation: Run it only in repositories you intend to analyze, and review generated reports before sharing them outside the project. <br>
Risk: Some commands query npm for package versions, deprecation status, and advisories. <br>
Mitigation: Use it only in environments where outbound npm registry lookups are allowed, or skip npm-backed checks when network access is restricted. <br>
Risk: Upgrade and replacement guidance can be incomplete because breaking-change detection relies on semver conventions, npm metadata, and local usage patterns. <br>
Mitigation: Treat plans as decision support, then confirm with release notes, run the project's tests, and review impacted code manually before changing dependencies. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Human-readable reports, Markdown, JSON report shapes, and inline shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include exit-code guidance for CI use; does not execute tests.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

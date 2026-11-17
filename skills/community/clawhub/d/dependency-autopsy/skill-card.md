## Description:

Deep health analysis of your dependency tree that helps assess abandonment risk, maintainer activity, unused package weight, replacement difficulty, version health, license compatibility, and dependency depth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcools1977](https://clawhub.ai/user/jcools1977)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to review package manifests and dependency trees for supply-chain health, maintainability risk, license concerns, bloat, and upgrade or replacement planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect dependency manifests and package-health signals from a project.

Mitigation: Use it only in projects where dependency metadata may be reviewed by the agent, and review the generated report before acting on recommendations.

Risk: Dependency health recommendations can be incomplete or misleading if package metadata is stale or project usage is unusual.

Mitigation: Validate critical replacement, upgrade, and license decisions against authoritative package, repository, and legal sources before making production changes.

## Reference(s):

- [Dependency Autopsy ClawHub skill page](https://clawhub.ai/jcools1977/skills/dependency-autopsy)
- [jcools1977 ClawHub publisher profile](https://clawhub.ai/user/jcools1977)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance]

**Output Format:** [Markdown dependency health report with scores, findings, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external API calls or credential requirements are indicated by the release evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

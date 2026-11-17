## Description:

Evaluate AI infrastructure scan results against security and regulatory frameworks, enforce policy-as-code, and generate SBOMs and compliance reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msaad00](https://clawhub.ai/user/msaad00)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and security or compliance engineers use the skill to assess AI infrastructure scan results against frameworks, enforce custom policies, generate SBOMs, and run optional CIS checks. Most evaluations run locally; CIS checks use locally configured cloud credentials for read-only provider API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An SBOM example may write sbom.json even though the metadata declares no file writes.

Mitigation: Check the output destination before generating an SBOM and confirm it is the intended location.

## Reference(s):

- [Project homepage](https://github.com/koda-ai-studio/agent-bom)
- [PyPI package](https://pypi.org/project/agent-bom/)
- [OpenSSF Scorecard](https://securityscorecards.dev/viewer/?uri=github.com/koda-ai-studio/agent-bom)
- [ClawHub skill page](https://clawhub.ai/msaad00/skills/agent-bom-compliance)

## Skill Output:

**Output Type(s):** [Analysis, Files, JSON, Markdown]

**Output Format:** [Compliance findings and reports, plus CycloneDX or SPDX SBOM files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the supplied scan data, selected frameworks, and optional CIS checks.]

## Skill Version(s):

0.115.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

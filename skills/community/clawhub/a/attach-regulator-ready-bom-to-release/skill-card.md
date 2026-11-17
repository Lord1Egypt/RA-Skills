## Description:

Attaches the exact CycloneDX or SPDX SBOM to a software release and helps assess document conformance, PURL syntax, SPDX license identifiers, required fields, detected format, specification version, BSI version-floor readiness, and release-to-release SBOM drift.

This skill is ready for commercial/non-commercial use.

## Publisher:

[powmcp](https://clawhub.ai/user/powmcp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, release engineers, and compliance reviewers use this skill to validate the exact SBOM intended for a software release before attachment. It helps document automated conformance findings while keeping vulnerability, supplier coverage, recursive resolution, and conformity-assessment work separate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Attached or fetched SBOM contents may be sent to PowMCP's hosted validation service.

Mitigation: Use public or organization-approved SBOMs with the hosted service, and use the documented local or CI validation path for confidential or pre-release artifacts.

Risk: The install command uses an unpinned npx package path.

Mitigation: Avoid running the installer from an elevated shell and review or pin the package source according to organizational policy before installation.

Risk: A clean conformance result can be mistaken for vulnerability clearance or complete supply-chain coverage.

Mitigation: Keep CSAF or VEX vulnerability statements, supplier coverage review, recursive component resolution, and conformity-assessment work as separate release checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/powmcp/skills/attach-regulator-ready-bom-to-release)
- [SBOM Check reference](artifact/references/sbom-preflight.md)
- [PowMCP SBOM Preflight MCP endpoint](https://powmcp.com/sbom-preflight/mcp)
- [PowMCP account limits](https://powmcp.com/account/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with checklist items, measured findings, disposition, and release handoff notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include exact tool-returned findings, BSI version-floor disposition, not-checked items, and comparison summaries when two release SBOMs are assessed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

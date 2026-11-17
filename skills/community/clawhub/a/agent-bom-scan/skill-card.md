## Description:

Checks a specified package version, repository, container image, or SBOM for vulnerabilities and inspects named CVEs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msaad00](https://clawhub.ai/user/msaad00)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and security engineers use the skill to assess vulnerabilities in a named software package or an explicitly selected repository, image, SBOM, or advisory. It can also produce SBOMs and remediation guidance for the requested target.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Online vulnerability lookups send package identifiers, versions, and advisory IDs to external providers; these identifiers may be sensitive for private packages.

Mitigation: Confirm permission before querying private package identifiers. Use offline mode when online requests are not authorized and report any resulting coverage gaps.

Risk: Explicit local MCP-client discovery can involve agent configuration paths that may contain sensitive settings.

Mitigation: Perform discovery only when explicitly requested, read only authorized targets, and do not print credentials or upload configuration contents.

## Reference(s):

- [agent-bom project and source](https://github.com/koda-ai-studio/agent-bom)
- [agent-bom on PyPI](https://pypi.org/project/agent-bom/)
- [OpenSSF Scorecard](https://securityscorecards.dev/viewer/?uri=github.com/koda-ai-studio/agent-bom)
- [Credential redaction implementation reference](https://github.com/koda-ai-studio/agent-bom/blob/main/src/agent_bom/security.py)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, JSON, Markdown, SBOM files]

**Output Format:** [Text findings and guidance; reports or SBOMs can be produced in JSON, SARIF, Markdown, CycloneDX, or SPDX formats.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the supplied target and available advisory data; offline scans can have incomplete vulnerability coverage.]

## Skill Version(s):

0.115.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

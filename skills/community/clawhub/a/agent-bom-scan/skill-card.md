## Description:

Checks specified packages, repositories, container images, SBOMs, and CVEs for vulnerabilities, and discovers local MCP clients only when explicitly requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msaad00](https://clawhub.ai/user/msaad00)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and security engineers use the skill to assess vulnerabilities in explicitly named packages, repositories, container images, SBOMs, or CVEs, and to generate SBOMs for requested projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may access local agent configuration paths during explicitly requested client discovery, and online vulnerability lookups send package identifiers, versions, and advisory IDs to providers.

Mitigation: Limit discovery to the requested clients; confirm before sending private package identifiers to online providers, or use offline mode and report its coverage gaps.

## Reference(s):

- [Project homepage](https://github.com/koda-ai-studio/agent-bom)
- [agent-bom on PyPI](https://pypi.org/project/agent-bom/)
- [SecurityScorecard](https://securityscorecards.dev/viewer/?uri=github.com/koda-ai-studio/agent-bom)
- [ClawHub release page](https://clawhub.ai/msaad00/skills/agent-bom-scan)

## Skill Output:

**Output Type(s):** [Analysis, Files, JSON, Markdown, Shell commands]

**Output Format:** [Vulnerability findings and guidance; reports in JSON, SARIF, HTML, or Markdown; SBOMs in CycloneDX or SPDX formats.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline scans may have incomplete advisory coverage; report and SBOM files are written to requested paths.]

## Skill Version(s):

0.115.6 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

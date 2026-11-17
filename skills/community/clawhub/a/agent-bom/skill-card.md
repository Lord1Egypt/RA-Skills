## Description:

agent-bom helps agents assess AI agent infrastructure for MCP discovery, package and container CVEs, SBOMs, CIS benchmarks, compliance, runtime exposure, and AI supply chain risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msaad00](https://clawhub.ai/user/msaad00)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and security engineers use this skill to inspect agentic infrastructure, discover MCP clients and servers, check dependencies and container images for vulnerabilities, generate SBOMs, evaluate compliance frameworks, and reason about blast radius. Cloud CIS checks, proxy enforcement, and dashboards should be invoked explicitly because they may touch local credentials or expose local state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill installs and runs an external package before handling sensitive local agent configuration.

Mitigation: Pin agent-bom to version 0.76.4, run it in an isolated environment, and verify the package with an independent trusted verifier before scanning configuration files.

Risk: The skill can inspect many local AI tool configuration paths during discovery and scan workflows.

Mitigation: Run only the specific scan needed, review the documented file-read scope first, and avoid broad discovery on sensitive environments without explicit approval.

Risk: CVE enrichment may disclose public package names or CVE IDs to vulnerability databases.

Mitigation: Use networked vulnerability enrichment only when that disclosure is acceptable, and restrict scans to the packages or artifacts required for the task.

Risk: Cloud CIS, proxy, and dashboard actions can use local credentials or expose local runtime state when explicitly invoked.

Mitigation: Confirm cloud, proxy, and dashboard actions separately, prefer read-only scoped credentials for cloud checks, and bind dashboard or proxy workflows to local-only access unless reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/msaad00/skills/agent-bom)
- [Project homepage](https://github.com/msaad00/agent-bom)
- [PyPI package](https://pypi.org/project/agent-bom/)
- [OpenSSF Scorecard](https://securityscorecards.dev/viewer/?uri=github.com/msaad00/agent-bom)
- [Credential redaction implementation](https://github.com/msaad00/agent-bom/blob/main/src/agent_bom/security.py#L159)
- [Configuration discovery implementation](https://github.com/msaad00/agent-bom/blob/main/src/agent_bom/discovery/__init__.py)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline command examples, concise security findings, remediation guidance, and optional JSON or SBOM references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local agent-bom commands and configuration snippets; artifact instructions state that scans and diagnostics should be read-only unless a user explicitly starts optional proxy, cloud, or dashboard workflows.]

## Skill Version(s):

0.76.4 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

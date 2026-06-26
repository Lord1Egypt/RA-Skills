## Description: <br>
Open security scanner for agentic infrastructure, including agents, MCP, packages, blast radius, runtime trust, package CVEs, container images, provenance, filesystems, and SBOMs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[msaad00](https://clawhub.ai/user/msaad00) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and security engineers use this skill to check packages and containers for vulnerabilities, inspect agent and MCP dependency exposure, verify package provenance, generate SBOMs, and produce remediation-oriented security findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad scan requests can read local agent, MCP, and related configuration files disclosed by the skill. <br>
Mitigation: Invoke the skill only for explicit package, image, dependency, SBOM, provenance, or agent/MCP scans and confirm scope before broad local scans. <br>
Risk: Vulnerability lookups send public package names and CVE IDs to external vulnerability databases. <br>
Mitigation: Use the skill when those lookups are acceptable for the intended environment, and avoid including secrets or private configuration contents in prompts or scan inputs. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/msaad00/agent-bom) <br>
- [PyPI project: agent-bom](https://pypi.org/project/agent-bom/) <br>
- [OpenSSF Scorecard: msaad00/agent-bom](https://securityscorecards.dev/viewer/?uri=github.com/msaad00/agent-bom) <br>
- [Credential redaction reference](https://github.com/msaad00/agent-bom/blob/main/src/agent_bom/security.py#L159) <br>
- [OSV vulnerability database API](https://api.osv.dev/v1) <br>
- [NVD CVE API](https://services.nvd.nist.gov/rest/json/cves/2.0) <br>
- [FIRST EPSS API](https://api.first.org/data/v1/epss) <br>
- [GitHub Security Advisories API](https://api.github.com/advisories) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, SARIF, HTML, and CycloneDX/SPDX SBOM formats depending on the workflow and consumer.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce vulnerability findings, provenance checks, blast-radius analysis, remediation plans, inventory summaries, diff reports, and CI gate results.] <br>

## Skill Version(s): <br>
0.89.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

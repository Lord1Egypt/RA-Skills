## Description: <br>
Open security scanner for agentic infrastructure across agents, MCP servers, packages, blast radius, runtime, trust, compliance, SBOMs, cloud CIS benchmarks, AISVS v1.0, MAESTRO layer tagging, and vector database security checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[msaad00](https://clawhub.ai/user/msaad00) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and security engineers use this skill to inventory local AI and MCP infrastructure, scan for vulnerabilities, generate SBOMs, assess compliance posture, and guide remediation planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect local AI-tool and MCP configuration paths when discovery or scanning is requested. <br>
Mitigation: Run it only with clear intent and reviewed scope; inspect the listed file paths before discovery. <br>
Risk: Package names and CVE IDs may be sent to vulnerability intelligence services during vulnerability lookup. <br>
Mitigation: Use the skill only when those identifiers are acceptable to query externally, and avoid including secrets or internal-only data in scan inputs. <br>
Risk: Optional cloud CIS benchmarks use locally configured cloud credentials. <br>
Mitigation: Use least-privilege read-only credentials and require explicit confirmation before cloud benchmarks. <br>
Risk: Broad directory scans, proxy mode, or dashboard startup can expand the operational scope of the tool. <br>
Mitigation: Require explicit confirmation before those actions and review the requested target scope. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/msaad00/agent-bom) <br>
- [Source Repository](https://github.com/msaad00/agent-bom) <br>
- [PyPI Package](https://pypi.org/project/agent-bom/) <br>
- [OpenSSF Scorecard](https://securityscorecards.dev/viewer/?uri=github.com/msaad00/agent-bom) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration snippets, and report-oriented text or JSON references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide generation of SBOM, compliance, scan, trust, and remediation outputs from agent-bom commands.] <br>

## Skill Version(s): <br>
0.76.4 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

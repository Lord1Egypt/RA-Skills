## Description: <br>
AI runtime security monitoring for context graph analysis, runtime audit log correlation with CVE findings, and vulnerability analytics queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[msaad00](https://clawhub.ai/user/msaad00) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and security engineers use this skill to inspect agent runtime context graphs, correlate user-provided audit logs with CVE findings, and query vulnerability analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit logs can contain sensitive runtime details or credential environment variable names. <br>
Mitigation: Provide only audit logs intended for analysis and verify that raw credential values are not included. <br>
Risk: Optional ClickHouse analytics introduces operator-managed persistence. <br>
Mitigation: Enable ClickHouse only when needed, configure credentials explicitly, and set retention according to the deployment policy. <br>
Risk: Installation depends on trusting the published PyPI package source. <br>
Mitigation: Confirm the package source before installation and install with the documented pip or pipx package name. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/msaad00/agent-bom-runtime) <br>
- [agent-bom homepage](https://github.com/msaad00/agent-bom) <br>
- [agent-bom PyPI package](https://pypi.org/project/agent-bom/) <br>
- [OpenSSF Scorecard viewer](https://securityscorecards.dev/viewer/?uri=github.com/msaad00/agent-bom) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference user-provided audit log paths and optional analytics configuration.] <br>

## Skill Version(s): <br>
0.89.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

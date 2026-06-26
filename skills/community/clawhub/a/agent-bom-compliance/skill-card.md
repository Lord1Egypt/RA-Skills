## Description: <br>
AI compliance and policy engine that evaluates scan results against OWASP, NIST, SOC 2, ISO 27001, CMMC, EU AI Act, AISVS v1.0, and related frameworks, and generates SBOMs and compliance reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[msaad00](https://clawhub.ai/user/msaad00) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers, security engineers, and compliance teams use this skill to evaluate AI infrastructure scan results against security and regulatory frameworks, enforce policy-as-code checks, run optional CIS benchmark checks, and generate CycloneDX or SPDX SBOMs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional CIS benchmark checks can read cloud account configuration through existing AWS, Azure, GCP, or Snowflake credentials. <br>
Mitigation: Run CIS checks only in approved accounts where read-only audit access is appropriate. <br>
Risk: Compliance, policy, and SBOM results depend on user-provided scan data, SBOMs, and policy files. <br>
Mitigation: Review input files and policy rules before relying on generated reports for compliance decisions. <br>


## Reference(s): <br>
- [Source repository](https://github.com/msaad00/agent-bom) <br>
- [PyPI package](https://pypi.org/project/agent-bom/) <br>
- [OpenSSF Scorecard](https://securityscorecards.dev/viewer/?uri=github.com/msaad00/agent-bom) <br>
- [ClawHub skill page](https://clawhub.ai/msaad00/agent-bom-compliance) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline shell commands, JSON policy examples, and SBOM/report file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce CycloneDX or SPDX SBOM files and compliance export formats selected by the operator.] <br>

## Skill Version(s): <br>
0.89.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

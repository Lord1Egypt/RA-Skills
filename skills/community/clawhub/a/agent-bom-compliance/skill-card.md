## Description: <br>
agent-bom compliance evaluates AI infrastructure scan results against security and regulatory frameworks, enforces policy-as-code rules, and generates SBOMs and compliance reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[msaad00](https://clawhub.ai/user/msaad00) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers, security engineers, and compliance teams use this skill to run local AI compliance checks, evaluate policy-as-code rules, generate SBOMs, and produce reports for frameworks such as OWASP, NIST, SOC 2, ISO 27001, CMMC, EU AI Act, and AISVS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad compliance trigger words and external package installation can cause users to invoke a larger workflow than intended. <br>
Mitigation: Install only when agent-bom is needed for compliance or SBOM work, and confirm the requested framework or report scope before running checks. <br>
Risk: Optional CIS benchmark checks can call AWS, Azure, GCP, or Snowflake APIs using locally configured credentials. <br>
Mitigation: Treat CIS checks as explicit actions, use read-only cloud roles, do not paste secrets into chat, and confirm the provider and scope before allowing cloud API calls. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/msaad00/skills/agent-bom-compliance) <br>
- [Project homepage](https://github.com/msaad00/agent-bom) <br>
- [PyPI package](https://pypi.org/project/agent-bom/) <br>
- [OpenSSF Scorecard](https://securityscorecards.dev/viewer/?uri=github.com/msaad00/agent-bom) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated CycloneDX or SPDX JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May optionally perform user-initiated, read-only cloud CIS benchmark checks when local cloud credentials are configured.] <br>

## Skill Version(s): <br>
0.91.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

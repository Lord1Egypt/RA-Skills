## Description:

Evaluates AI infrastructure scan results against security and regulatory frameworks, checks policy-as-code rules, and generates SBOMs and compliance reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msaad00](https://clawhub.ai/user/msaad00)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers, security engineers, and compliance teams use the skill to assess AI infrastructure scan results against frameworks such as OWASP, NIST, SOC 2, ISO 27001, and the EU AI Act; enforce custom policies; and generate compliance reports or SBOMs. Optional CIS checks can query cloud accounts when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional CIS checks access cloud account information through read-only API calls using configured credentials.

Mitigation: Run CIS checks only when requested and use operator-configured credentials with the minimum permissions needed; never paste secrets into prompts or expose them in output.

## Reference(s):

- [Project homepage](https://github.com/koda-ai-studio/agent-bom)
- [PyPI package](https://pypi.org/project/agent-bom/)
- [OpenSSF Scorecard](https://securityscorecards.dev/viewer/?uri=github.com/koda-ai-studio/agent-bom)
- [ClawHub skill page](https://clawhub.ai/msaad00/skills/agent-bom-compliance)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON]

**Output Format:** [Compliance findings and reports in text or Markdown; SBOMs in CycloneDX or SPDX JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Frameworks, policy rules, SBOM format, and optional cloud provider are selected for each request.]

## Skill Version(s):

0.115.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

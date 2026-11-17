## Description:

物料清单漏洞情报专业版 helps enterprise security teams generate and compare SBOMs, query OSV/GHSA/NVD vulnerability data, run batch dependency scans, and produce monitoring, alerting, SARIF, and reporting guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Security teams and developers use this skill to generate CycloneDX/SPDX SBOMs, check dependency vulnerabilities across npm, Python, Go, Cargo, Maven, and NuGet projects, and connect findings to CI/CD or monitoring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The command-executing skill has broad activation text that could pull it into unrelated operations work.

Mitigation: Use it only for SBOM, dependency inventory, and vulnerability intelligence tasks, and review proposed commands before execution.

Risk: Dependency names, versions, and project inventory data may be sent to OSV, NVD, or configured alert webhooks.

Mitigation: Use approved internal scanners or mirrors for private inventories, and do not place real webhook URLs, API keys, or tokens inline.

Risk: Local scanner commands and report generation can create files or run package-manager tooling in project directories.

Mitigation: Run scans in a controlled workspace with approved tools and least-privilege access, especially for enterprise repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/bom-vuln-intel-tool-pro)
- [OSV query API](https://api.osv.dev/v1/query)
- [NVD CVE API](https://services.nvd.nist.gov/rest/json/cves/2.0)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell, Python, YAML, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local scanner commands, SBOM files, vulnerability reports, SARIF/HTML/PDF report guidance, and webhook monitoring configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

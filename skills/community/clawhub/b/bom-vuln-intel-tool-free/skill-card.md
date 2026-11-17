## Description:

软件物料清单(SBOM)生成与依赖漏洞检查工具，支持基础 npm 和 pip 包扫描、SBOM 生成，以及 OSV/GHSA 漏洞查询，适合个人开发者日常使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security-conscious project maintainers use this skill to inspect npm and pip dependencies, create a basic SBOM, and check known package vulnerabilities before updating or introducing dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package names and versions from private projects may be sent to public package and vulnerability services.

Mitigation: Review or redact dependency names before running checks on private or embargoed projects.

Risk: Generated shell commands may behave unexpectedly on unusual package names or project files.

Mitigation: Inspect proposed commands before execution and run them in a controlled project workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/bom-vuln-intel-tool-free)
- [OSV API](https://api.osv.dev)
- [npm Registry](https://registry.npmjs.org)
- [PyPI JSON API](https://pypi.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local SBOM JSON and vulnerability-check output when the agent runs the proposed commands.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Scans C and Python code for security risks, audits dependencies, looks up CWE/CVE context, and generates structured security reports using local static analysis with optional LLM-assisted semantic analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a9320](https://clawhub.ai/user/a9320)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to scan source trees for code vulnerabilities, dependency risks, and CWE/CVE context, then receive JSON or Markdown-ready findings with severity, evidence, and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional AI analysis can send full source files to the configured LLM provider.

Mitigation: Keep enable_ai=false for sensitive repositories, or configure a local LLM backend before scanning private code.

Risk: Saved scan memory under ~/.coderisk/memory can influence later findings.

Mitigation: Inspect, reset, or clear the memory directory when running independent reviews or when prior scan results should not affect new analysis.

## Reference(s):

- [Server-resolved GitHub import](https://github.com/a9320/code-risk-agent/tree/master/skill)
- [ClawHub skill page](https://clawhub.ai/a9320/skills/code-risk-agent)
- [Publisher profile](https://clawhub.ai/user/a9320)
- [MITRE CWE definitions](https://cwe.mitre.org/data/definitions/)
- [NVD vulnerability details](https://nvd.nist.gov/vuln/detail/)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Code, Shell commands, Guidance]

**Output Format:** [Structured JSON reports with Markdown summaries and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include severity breakdowns, CWE/CVE links, file and line locations, evidence sources, and suggested fixes.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter 1.0.0 and package.json 1.0.4 differ)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

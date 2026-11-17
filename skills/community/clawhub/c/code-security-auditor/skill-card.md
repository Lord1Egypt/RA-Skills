## Description:

Comprehensive code security audit with AI-powered vulnerability detection that covers OWASP Top 10, dependency scanning, secret detection, SAST, and actionable fix recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zenmejiang-commits](https://clawhub.ai/user/zenmejiang-commits)

### License/Terms of Use:

MIT

## Use Case:

Developers and security engineers use this skill to audit repositories for common application security issues, dependency vulnerabilities, leaked secrets, insecure configuration, and remediation guidance. It is suited for pre-release review, CI checks, and security-focused code assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote LLM integrations can send source-derived prompts to Qwen or ChatGLM providers when enabled.

Mitigation: Use the default local scanner path for sensitive repositories and enable remote providers only after confirming the data-sharing posture is acceptable.

Risk: The iteration script can write persistent agent learning state.

Mitigation: Do not run iterate.sh unless persistent writes to shared OpenClaw learning state are acceptable for the environment.

Risk: Automated security analysis may miss vulnerabilities or produce findings that need expert judgment.

Mitigation: Review scanner results before acting on them and combine this skill with human security review for production releases.

## Reference(s):

- [OWASP Top 10 Reference](references/owasp-top10.md)
- [Codex Security Comparison](references/codex-security-comparison.md)
- [OWASP Top 10 2021](https://owasp.org/www-project-top-ten/)
- [CWE Common Weakness Enumeration](https://cwe.mitre.org/)
- [NVD Vulnerability Database](https://nvd.nist.gov/)
- [CVE Program](https://cve.mitre.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, SARIF, and terminal text with inline code and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include vulnerability findings, severity summaries, evidence snippets, remediation guidance, and CI-oriented outputs.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

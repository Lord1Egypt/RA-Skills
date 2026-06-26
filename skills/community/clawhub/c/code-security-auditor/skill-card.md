## Description: <br>
Comprehensive code security audit with AI-powered vulnerability detection. Covers OWASP Top 10, dependency scanning, secret detection, SAST, and provides actionable fix recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zenmejiang-commits](https://clawhub.ai/user/zenmejiang-commits) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, security engineers, and reviewers use this skill to audit codebases for OWASP Top 10 issues, dependency vulnerabilities, exposed secrets, static-analysis findings, and remediation guidance before release or during CI review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documentation overstates local-only privacy while optional Qwen and ChatGLM providers can transmit analyzed code to external services. <br>
Mitigation: Use the default local auditor path or local Ollama provider for sensitive code, and enable Qwen or ChatGLM only after explicit review and approval of external data transmission. <br>
Risk: The self-evaluation script can write persistent iteration reports and global learning-log entries. <br>
Mitigation: Run iterate.sh only in a controlled or disposable workspace after reviewing its filesystem writes, or avoid it for normal security-audit use. <br>
Risk: Automated vulnerability findings and generated remediation may be incomplete or incorrect. <br>
Mitigation: Treat reports and fix suggestions as review inputs, then validate material findings and code changes with human security review and project tests before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zenmejiang-commits/code-security-auditor) <br>
- [OWASP Top 10 Reference](references/owasp-top10.md) <br>
- [Codex Security Comparison](references/codex-security-comparison.md) <br>
- [Extended Security Rules](rules/extended-rules.md) <br>
- [OWASP Top 10 2021](https://owasp.org/www-project-top-ten/) <br>
- [CWE Common Weakness Enumeration](https://cwe.mitre.org/) <br>
- [National Vulnerability Database](https://nvd.nist.gov/) <br>
- [CVE Program](https://cve.mitre.org/) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, JSON, Markdown, or SARIF-style JSON reports with remediation examples and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write report files when an output path is provided; optional LLM-backed analysis can return JSON-like vulnerability assessments and fix suggestions.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

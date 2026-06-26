## Description: <br>
Privacy-first Spring Boot code health diagnosis that detects security vulnerabilities, performance anti-patterns, code quality issues, and dependency risks across Java/Spring Boot projects, then generates a structured health report with severity classification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sallyface0](https://clawhub.ai/user/sallyface0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to scan Java and Spring Boot projects for security, reliability, performance, design, dependency, and convention issues. It supports daily scans, pre-release reviews, and incremental checks by producing prioritized findings and remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional auto-fix or remediation behavior could modify project files if used without adequate review. <br>
Mitigation: Use any fix mode only when it is explicit, opt-in, and produces reviewable changes before they are applied. <br>
Risk: Generated reports may contain code snippets, file paths, or findings from the scanned project. <br>
Mitigation: Store reports only in the intended project location, control access to the report, and delete it when it is no longer needed. <br>


## Reference(s): <br>
- [Code Health Scanner on ClawHub](https://clawhub.ai/sallyface0/code-health-scanner) <br>
- [Java/Spring Detection Rules](references/rules/java-spring.md) <br>
- [Code Health Report Template](references/report-template.md) <br>
- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown health report with severity-ranked findings, code snippets, health score, and remediation recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report is written to the target project; low-risk fixes are optional and require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

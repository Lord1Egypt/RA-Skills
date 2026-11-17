## Description: <br>
Code Quality Paid guides enterprise development teams through code quality and security audits, including OWASP Top 10 checks, batch project review, custom rules, CI/CD integration, and SARIF, HTML, or JSON reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and DevSecOps teams use this skill to inspect repositories, run local audit commands, define custom quality and security rules, and produce reports for remediation or CI/CD workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to inspect source code and run local audit commands. <br>
Mitigation: Use it only on repositories you are authorized to scan and review commands before execution. <br>
Risk: Generated reports and CI artifacts may expose vulnerability details, file paths, or other sensitive project information. <br>
Mitigation: Review artifact visibility, retention, and access controls before enabling upload or sharing workflows. <br>
Risk: External scanner examples may require service tokens or API keys. <br>
Mitigation: Store credentials in environment variables or secret managers, and avoid writing real keys directly into configuration files. <br>


## Reference(s): <br>
- [SkillHub homepage](https://skillhub.cn) <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/code-quality-paid) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell, YAML, Python, and JSON examples; reports may be SARIF, HTML, JSON, or text summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local audit reports and CI artifacts for review.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

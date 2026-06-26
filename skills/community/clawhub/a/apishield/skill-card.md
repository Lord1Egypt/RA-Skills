## Description: <br>
API endpoint security auditor — scans route definitions for missing auth, rate limiting, CORS issues, and input validation holes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use APIShield to scan local API route definitions for missing authentication, rate limiting, CORS issues, input validation gaps, exposed debug endpoints, and related API security findings. It can also generate markdown reports, endpoint inventories, OWASP API Top 10 mappings, and optional pre-commit checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hook installation modifies the target repository by adding or updating lefthook-based pre-commit checks. <br>
Mitigation: Run hook installation only when you intentionally want APIShield checks added to the repository, and review the resulting lefthook.yml. <br>
Risk: Generated audit reports may include local file paths, endpoint names, security scores, and vulnerability descriptions. <br>
Mitigation: Review APISHIELD-REPORT.md before committing, sharing, or publishing it. <br>
Risk: License keys are sensitive credentials used through APISHIELD_LICENSE_KEY or OpenClaw configuration. <br>
Mitigation: Store license keys in local environment or user configuration and avoid committing them to source control. <br>
Risk: Regex-based local scanning can miss framework-specific behavior or produce findings that need human review. <br>
Mitigation: Use scan results as a local audit aid and validate important findings before relying on them for release or compliance decisions. <br>


## Reference(s): <br>
- [APIShield website](https://apishield.pages.dev) <br>
- [APIShield pricing](https://apishield.pages.dev/#pricing) <br>
- [ClawHub APIShield listing](https://clawhub.ai/suhteevah/apishield) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/suhteevah) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and Markdown reports with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write APISHIELD-REPORT.md for reports and lefthook.yml when hook installation is explicitly invoked.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Audits GitHub repositories or local directories for malicious code, backdoors, suspicious behavior, and supply-chain risk before a user trusts or installs them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alondotsh](https://clawhub.ai/user/alondotsh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and agent operators use this skill to perform static-first security triage of GitHub repositories or local codebases before installation, trust, or deeper investigation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may clone a user-specified GitHub repository, including over SSH if the user supplies an SSH URL. <br>
Mitigation: Prefer HTTPS repository URLs when SSH credentials should not be involved, and audit only repositories the user intentionally selects. <br>
Risk: Online dependency vulnerability intelligence can share dependency metadata with external vulnerability sources. <br>
Mitigation: Use the default offline static audit unless the user explicitly approves online vulnerability lookups. <br>
Risk: The skill writes audit reports to disk and reads the selected target project. <br>
Mitigation: Run it only on intended repositories or local directories and review the configured report directory before use. <br>
Risk: The evidence includes capability tags for wallet, purchase, and sensitive-credential scenarios, but the security guidance says the artifacts do not justify providing those credentials. <br>
Mitigation: Do not provide wallet, payment, or unrelated sensitive credentials while using this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alondotsh/alon-github-security-audit) <br>
- [Project homepage](https://github.com/alondotsh/alon-skills/tree/master/skills/alon-github-security-audit) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown security audit report with verdicts, findings, and optional shell commands for cloning or cleanup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a structured report to a local audit directory.] <br>

## Skill Version(s): <br>
0.1.9 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

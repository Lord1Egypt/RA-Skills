## Description: <br>
Generate professional bug bounty reports for HackerOne, Bugcrowd, and other platforms with pre-filled templates, CWE mapping, reproduction steps, and severity assessment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hostilespider](https://clawhub.ai/user/hostilespider) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security researchers and bug bounty hunters use this skill to draft structured vulnerability reports for HackerOne, Bugcrowd, or generic disclosure workflows. It helps assemble report sections for summary, reproduction, proof of concept, impact, remediation, CWE mapping, and severity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may include incomplete placeholders or inaccurate vulnerability details if submitted without review. <br>
Mitigation: Review and complete the generated report before submitting it to a bug bounty program. <br>
Risk: Examples or proof-of-concept sections may accidentally include real secrets or sensitive tokens. <br>
Mitigation: Use redacted sample values and remove secrets from report examples before sharing. <br>
Risk: Using an existing output path can overwrite a local file. <br>
Mitigation: Choose the output path carefully and confirm it is safe to replace before running with --output. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hostilespider/bb-report-template) <br>
- [Publisher Profile](https://clawhub.ai/user/hostilespider) <br>
- [MITRE CWE](https://cwe.mitre.org/) <br>
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, guidance] <br>
**Output Format:** [Markdown report text, printed to stdout or written to a user-selected file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated report content includes placeholders that must be completed and reviewed before submission.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

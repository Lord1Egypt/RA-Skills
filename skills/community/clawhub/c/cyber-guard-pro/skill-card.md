## Description: <br>
An all-in-one cybersecurity assistant for vulnerability checks, phishing detection, password auditing, privacy exposure review, and compliance self-assessment for individuals and small businesses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and small business operators use this skill to triage phishing indicators, password strength, privacy exposure, vulnerability and configuration issues, and baseline compliance gaps. It produces prioritized remediation guidance for self-directed security review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security findings may be used for self-directed decisions without a professional audit. <br>
Mitigation: Treat results as triage guidance and have material systems reviewed by qualified security personnel before relying on them. <br>
Risk: Password, email, or account breach checks can expose sensitive inputs if handled carelessly. <br>
Mitigation: Avoid sharing real passwords; use password-manager audits or hashed checks, and confirm whether breach lookup methods are local-only or user-directed before submitting account data. <br>
Risk: Public breach database lookups may contact a third-party service. <br>
Mitigation: Assume external breach services may be used unless the agent confirms a local-only method, and avoid submitting sensitive account details unnecessarily. <br>


## Reference(s): <br>
- [Cyber Guard Pro on ClawHub](https://clawhub.ai/ai-gaoqian/cyber-guard-pro) <br>
- [ai-gaoqian publisher profile](https://clawhub.ai/user/ai-gaoqian) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown security report with findings, risk levels, scores, prioritized hardening checklist, and optional compliance status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May discuss hashes or public breach lookup workflows; users should avoid sharing real passwords.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Api Security Scanner helps agents review REST API endpoints and API configuration for common security issues, including OWASP API Top 10 risks, authentication and authorization flaws, sensitive data exposure, missing rate limits, and injection risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caingao](https://clawhub.ai/user/caingao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, API owners, and security teams use this skill to perform lightweight REST API security reviews before deployment, during design review, or when preparing structured security reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API descriptions, configuration snippets, or scan inputs may contain bearer tokens, API keys, session cookies, private keys, internal hostnames, customer data, or private vulnerability details. <br>
Mitigation: Redact or replace sensitive values before sharing inputs with the agent unless the user has approval to process them in the AI environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/caingao/api-security-scanner) <br>
- [API security scan rules](artifact/scan-rules.md) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown security review report with severity labels and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include findings grouped by authentication, authorization, input validation, data protection, rate limiting, and configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

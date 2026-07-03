## Description: <br>
Enterprise cybersecurity audit and hardening skill covering vulnerability scanning, compliance checks, TLS/SSL assessment, port scanning, ransomware defense planning, and structured security reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security engineers, compliance teams, and authorized operators use this skill to assess systems they own or have explicit permission to test, then generate prioritized hardening and compliance guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Intrusive scanning or penetration-testing assistance can affect systems or target assets without authorization. <br>
Mitigation: Use only on owned or explicitly authorized systems, define target scope before scanning, document permission, apply rate limits, and coordinate with monitoring teams. <br>
Risk: The skill may require OAuth tokens or sensitive credentials for audit workflows. <br>
Mitigation: Use least-privilege credentials, avoid exposing secrets in prompts or reports, store tokens securely, and rotate credentials after use when appropriate. <br>
Risk: Security findings or remediation guidance may be incomplete or misleading if accepted without review. <br>
Mitigation: Have qualified personnel review generated findings, validate evidence against authoritative tools, and prioritize remediation using organizational risk criteria. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and structured report guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce executive summaries, detailed findings with CVSS scores, remediation steps, compliance gap analysis, and report content for formats such as PDF, JSON, Excel, or Word.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

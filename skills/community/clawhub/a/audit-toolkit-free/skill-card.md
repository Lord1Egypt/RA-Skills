## Description: <br>
Audit Toolkit Free helps agents structure audit workflows for financial reconciliation, compliance review, technical security review, and AI ethics assessment using evidence collection, discrepancy analysis, and report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, finance teams, compliance reviewers, and AI product teams use this skill to organize audit requests, collect evidence, compare artifacts against standards or expectations, classify risks, and draft structured audit reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive audit data may be written into persistent local evidence logs without clear retention limits. <br>
Mitigation: Use only data the user is allowed to store locally, avoid secrets unless necessary, redact sensitive fields, and define retention and deletion rules before running audits. <br>
Risk: The skill requests broad write and exec authority and may use callback URLs. <br>
Mitigation: Require explicit confirmation before shell commands or callback URL use, review command intent before execution, and restrict callbacks to trusted destinations. <br>
Risk: Generated audit reports can be mistaken for formal certification. <br>
Mitigation: Treat reports as templates and analysis guidance; require qualified human review before using findings as professional audit conclusions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/audit-toolkit-free) <br>
- [Skill Homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance, audit templates, command suggestions, and structured JSON-style result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include evidence logs, risk levels, findings, remediation suggestions, and callback URL handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

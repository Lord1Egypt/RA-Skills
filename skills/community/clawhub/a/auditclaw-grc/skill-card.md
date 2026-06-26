## Description: <br>
AI-native GRC (Governance, Risk, and Compliance) for OpenClaw that manages controls, evidence, risks, policies, vendors, incidents, assets, access reviews, questionnaires, reports, dashboards, trust center pages, and local security scans across 13 frameworks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mailnike](https://clawhub.ai/user/mailnike) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Compliance, security, and engineering teams use this skill to manage GRC workflows in OpenClaw, including framework activation, gap analysis, evidence tracking, risk and incident workflows, reporting, dashboards, and trust center generation. Developers and operators can also run local security header, SSL/TLS, and GDPR checks against systems they are authorized to assess. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may request high-value cloud, identity, or source-control credentials for optional integrations. <br>
Mitigation: Use least-privilege read-only roles, prefer local environment variables or a secret manager, and do not paste service-account JSON, client secrets, or API tokens into chat. <br>
Risk: Companion integration scripts can connect to external cloud, GitHub, or identity-provider accounts. <br>
Mitigation: Verify companion skills before connection tests and confirm the exact permissions and target account before running integration checks. <br>
Risk: Security scans can assess live URLs and domains. <br>
Mitigation: Run scans only against systems the user owns or is authorized to assess. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mailnike/auditclaw-grc) <br>
- [AuditClaw Homepage](https://www.auditclaw.ai) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Declared Source Repository](https://github.com/avansaber/auditclaw-grc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown summaries and guidance, shell commands for local scripts, JSON parsed into human-readable responses, and generated local files such as HTML reports, dashboards, trust center pages, and ZIP evidence exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local SQLite state and optional browser, cloud, GitHub, and identity-provider integrations when configured by the user.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata; artifact frontmatter declares 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

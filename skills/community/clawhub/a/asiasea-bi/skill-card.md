## Description: <br>
A Feishu-integrated BI data gateway for switching across enterprise systems, querying real API-backed business metrics from natural-language time ranges, and publishing visual report snapshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ASAzhangyongchao](https://clawhub.ai/user/ASAzhangyongchao) <br>

### License/Terms of Use: <br>
Jindengta BI Skill Proprietary and Confidential License <br>


## Use Case: <br>
Authorized Asiasea or related enterprise users use this skill to initialize access, select a business domain, query finance or business metrics such as reimbursements and department budgets, and receive dashboard-style summaries and report links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle and publish sensitive business data with reusable API authorization headers. <br>
Mitigation: Install only in authorized environments, remove authorization headers from generated HTML, and verify report access controls before production use. <br>
Risk: Session-file persistence can retain user-specific system context and authorization material. <br>
Mitigation: Secure or disable session-file persistence, restrict filesystem access, and clear session files according to the deployment's retention policy. <br>
Risk: Generated dashboards and archive publishing can expose business reports beyond the intended audience. <br>
Mitigation: Require explicit user confirmation before upload or publishing and validate the destination's access policy before sharing report links. <br>
Risk: The server-resolved provenance for this release is unavailable. <br>
Mitigation: Confirm package provenance and publisher authorization before relying on the skill in production. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ASAzhangyongchao/asiasea-bi) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, HTML reports, URLs] <br>
**Output Format:** [Markdown responses with metric summaries and links to generated HTML dashboards] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call enterprise APIs, persist per-user session state, upload report snapshots, and publish report URLs when authorized.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Generates configuration baseline health checks and remediation deliverables for contracted Alibaba Cloud customers across WAF 3.0, SAS, Cloud Firewall, and DDoS Protection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer success, delivery, and presales teams use this skill to assess Alibaba Cloud security product configuration coverage, score posture against baseline checks, and prepare remediation actions for customer reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Collector scripts rely on Alibaba Cloud CLI credentials for read-only collection, and broad production administrator credentials could expose more data than needed. <br>
Mitigation: Use a dedicated read-only RAM sub-account with only the documented product policies, review the collected JSON before sharing it, and avoid broad production admin credentials. <br>
Risk: Generated reports and intermediate JSON can contain customer security posture and asset configuration details. <br>
Mitigation: Store and share the generated JSON, HTML, XLSX, and Markdown outputs according to customer confidentiality requirements, and review them before external delivery. <br>
Risk: The scoring workflow may install the documented Python packages when dependencies are missing. <br>
Mitigation: Run the skill in an isolated environment when possible and review the declared requirements before allowing dependency installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-security-health-check) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [WAF Checks](references/checks/waf.yaml) <br>
- [SAS Checks](references/checks/sas.yaml) <br>
- [Cloud Firewall Checks](references/checks/cfw.yaml) <br>
- [DDoS Checks](references/checks/ddos.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Local JSON, HTML, XLSX, and Markdown files plus shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates scores.json, health-report.html, remediation.xlsx, and exec-summary.md from customer-provided or locally collected JSON.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

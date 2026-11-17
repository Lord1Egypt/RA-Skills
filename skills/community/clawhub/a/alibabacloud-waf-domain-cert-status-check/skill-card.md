## Description:

Inventories certificates on Alibaba Cloud WAF CNAME-access domains, identifies expired or expiring certificates, and provides read-only renewal guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and support engineers use this skill to audit certificate expiry across Alibaba Cloud WAF 2.0 and 3.0 CNAME-access domains and prioritize manual renewal without changing cloud resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance includes privileged CLI installation, remote script execution, and automatic plugin updates.

Mitigation: Prefer an administrator-managed, preinstalled Aliyun CLI; avoid curl-to-shell and self-update, and disable broad automatic plugin installation where possible.

Risk: Access to WAF domain and certificate metadata through an Alibaba Cloud profile may expose sensitive inventory or exceed the audit's needs.

Mitigation: Use least-privilege temporary or role-based credentials limited to the documented WAF and CAS read actions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/sdk-team/skills/alibabacloud-waf-domain-cert-status-check)
- [Certificate status and classification](artifact/references/cert-status-basics.md)
- [Read-only RAM permissions](artifact/references/ram-policies.md)
- [Verification method](artifact/references/verification-method.md)
- [WAF 3.0 CNAME domain configuration](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/add-a-domain-name-to-waf-in-cname-record-mode)
- [CAS certificate detail API](https://api.aliyun.com/document/cas/2020-04-07/GetUserCertificateDetail)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown summary table with prioritized action items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports domain, certificate identity, expiry, days remaining, and status; omits certificate contents and private keys.]

## Skill Version(s):

0.0.1 (source: ClawHub release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

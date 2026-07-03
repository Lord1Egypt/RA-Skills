## Description: <br>
Diagnoses DNS resolution failures, domain unreachable issues, NXDOMAIN errors, DNS record propagation delays, DNS hijacking, and other DNS-layer problems using scripted checks across Alibaba Cloud DNS, GTM, PrivateZone, and third-party DNS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud support engineers, DNS administrators, and developers use this skill to collect and interpret DNS diagnostic evidence for Alibaba Cloud DNS, GTM, PrivateZone, and third-party DNS incidents. It is intended for guided troubleshooting of resolution failures, propagation delays, NXDOMAIN responses, and suspected DNS hijacking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup commands and Aliyun plugin operations can change the local tool environment. <br>
Mitigation: Review setup commands before execution and avoid letting the agent update or install Aliyun plugins automatically. <br>
Risk: Cloud API diagnostics require sensitive credentials and can expose more account scope than needed. <br>
Mitigation: Use a least-privilege read-only DNS RAM role and never enter secrets on command lines or in chat. <br>
Risk: Public DNS, WHOIS, or boce probing can disclose internal or sensitive domain names. <br>
Mitigation: Do not submit internal or sensitive domains or URLs to public services unless that disclosure is acceptable. <br>


## Reference(s): <br>
- [Skill Page](https://clawhub.ai/sdk-team/alibabacloud-dns-resolve-diagnose) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [API Reference](references/api-reference.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [Examples](references/examples.md) <br>
- [Related Commands](references/related-commands.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON diagnostic artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces read-only diagnostic guidance and may save intermediate JSON reports under temporary diagnostic directories.] <br>

## Skill Version(s): <br>
0.0.1-beta.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

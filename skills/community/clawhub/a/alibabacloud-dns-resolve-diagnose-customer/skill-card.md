## Description: <br>
A read-only Alibaba Cloud DNS diagnostic skill that helps investigate DNS resolution failures, unreachable domains, record propagation issues, NXDOMAIN, and related DNS-layer anomalies across Alibaba Cloud DNS, GTM, PrivateZone, and third-party DNS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External customers, developers, and DNS operators use this skill to run read-only DNS checks, compare authoritative and recursive resolution behavior, inspect Alibaba Cloud DNS configuration when read credentials are available, and produce diagnostic reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use credentialed Alibaba Cloud DNS, GTM, Domain, and PrivateZone read access. <br>
Mitigation: Use least-privilege read-only RAM permissions, prefer short-lived roles or profiles, and avoid broad or persistent access keys. <br>
Risk: DNS probes, WHOIS lookups, public resolver checks, and boce.aliyun.com probing can disclose tested domains to external services. <br>
Mitigation: Do not run the skill against sensitive internal hostnames unless the user has approved the probe destinations and data exposure. <br>
Risk: The setup flow may modify local Aliyun CLI plugin behavior and install Playwright browser dependencies. <br>
Mitigation: Review CLI plugin update settings and dependency installation commands before execution, and disable automatic plugin updates after use if required by local policy. <br>


## Reference(s): <br>
- [RAM Policies](references/ram-policies.md) <br>
- [DNS Diagnosis OpenAPI Reference](references/api-reference.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [DNS Diagnosis Case Studies](references/examples.md) <br>
- [Related CLI Commands](references/related-commands.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON diagnostic artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save raw diagnostic data under /tmp/dns_diag_<domain>/ and summarize script-generated DNS, WHOIS, OpenAPI, and probing results.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

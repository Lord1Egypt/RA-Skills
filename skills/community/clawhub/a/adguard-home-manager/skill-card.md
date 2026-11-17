## Description:

Manage AdGuard Home network-wide DNS ad blocking, including status checks, filtering statistics, custom DNS rules, query logs, and filtering controls for a self-hosted DNS server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kryzl19](https://clawhub.ai/user/kryzl19)

### License/Terms of Use:

MIT-0

## Use Case:

External users and administrators use this skill to inspect and manage an AdGuard Home instance from an agent workflow. It supports checking DNS filtering status, viewing statistics and logs, managing blocking rules, and enabling or disabling filtering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable or disable network-wide DNS filtering.

Mitigation: Limit toggle operations to trusted users and review filtering changes before and after execution.

Risk: Authentication uses Basic Auth and may be sent to non-local endpoints.

Mitigation: Prefer HTTPS for any non-local AdGuard Home URL and use a dedicated low-privilege account with a unique password.

Risk: DNS query logs can expose household or organizational browsing patterns.

Mitigation: Restrict query-log access to trusted workflows and avoid unattended log inspection.

Risk: Rule-management behavior may not match the documented DNS rewrite wording.

Mitigation: Manually verify add and remove results in AdGuard Home because the implementation appears to target filtering rules rather than DNS rewrite rules.

## Reference(s):

- [AdGuard Home project](https://github.com/Adguard/AdGuardHome)
- [AdGuard Home overview](https://adguard.com/adguard-home/overview.html)
- [AdGuard Home API configuration reference](https://github.com/AdguardTeam/AdGuardHome/wiki/Config#web-interface)
- [ClawHub skill page](https://clawhub.ai/kryzl19/skills/adguard-home-manager)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ADGUARD_USERNAME, ADGUARD_PASSWORD, ADGUARD_BASE_URL, curl, and jq.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

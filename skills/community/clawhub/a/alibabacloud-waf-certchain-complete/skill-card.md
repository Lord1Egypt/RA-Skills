## Description:

Checks Alibaba Cloud WAF certificate-chain completeness, repairs a supplied PEM bundle, and guides manual upload of the completed chain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and WAF administrators use this skill to check a known Alibaba Cloud WAF certificate or local PEM bundle, repair missing intermediate certificates, and prepare a complete chain for manual upload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Piping a downloaded CLI installer directly to a shell can execute unreviewed code.

Mitigation: Install Aliyun CLI through a trusted package manager or verified release instead of curl-to-bash.

Risk: Automatic plugin installation introduces an additional software trust boundary.

Mitigation: Enable automatic plugin installation only when you accept that trust boundary.

Risk: Hidden remote-probing flags can initiate outbound TLS connections outside the stated local-check scope.

Mitigation: Do not use the remote-probing flags unless you explicitly intend outbound TLS connections.

Risk: Broad cloud credentials increase exposure during certificate status checks.

Mitigation: Use a dedicated least-privilege WAF read-only profile.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-waf-certchain-complete)
- [Certificate-chain basics](artifact/references/certificate-chain-basics.md)
- [Aliyun CLI installation guide](artifact/references/cli-installation-guide.md)
- [Read-only RAM policy](artifact/references/ram-policies.md)
- [Related commands](artifact/references/related-commands.md)
- [Aliyun CLI releases](https://github.com/aliyun/aliyun-cli/releases)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Files]

**Output Format:** [Markdown guidance and a local PEM certificate-chain file when repaired]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports local and WAF-side status separately; certificate upload remains manual.]

## Skill Version(s):

0.0.1 (source: ClawHub release and references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

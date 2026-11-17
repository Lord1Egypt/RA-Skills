## Description:

Provides Alibaba Cloud Live-Debug runtime diagnostics for Java and Python, including probes, JVM commands, and capture-result queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and operations engineers use this skill to configure runtime diagnostics on Alibaba Cloud services and inspect captured results. It supports targeted probes for Java and Python, with JVM commands available for Java.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The partial security scan flags that probe creation may be treated as read-only and that example workflows may send unsanitized application return values to SLS.

Mitigation: Review probe creation and deletion authorization, confirm the exact targets and data captured or sent to SLS, and verify that the required CLI installation privileges are acceptable. Treat the scan as incomplete.

## Reference(s):

- [Live-Debug reference](references/live-debug.md)
- [RAM permissions reference](references/ram-policies.md)
- [Skill version manifest](references/manifest.json)
- [Alibaba Cloud CLI installation and update guide](https://www.alibabacloud.com/help/zh/cli/install-update-alibaba-cloud-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON configuration, Operational guidance]

**Output Format:** [Markdown guidance with shell commands and JSON task configurations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic task results returned by Alibaba Cloud services.]

## Skill Version(s):

0.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

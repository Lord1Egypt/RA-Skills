## Description:

Provides mirror-first download and configuration guidance for dependencies, tools, models, and SDKs in mainland China, with fallback and verification steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fjjzy](https://clawhub.ai/user/fjjzy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers working on mainland China networks use the skill to choose and configure regional mirrors, troubleshoot downloads, and verify or roll back changes across common package ecosystems.

### Deployment Geography for Use:

Mainland China

## Known Risks and Mitigations:

Risk: Examples may use trusted-host defaults or settings that affect more than the current task.

Mitigation: Remove trusted-host defaults, keep changes limited to the requested project or command, and approve permanent settings explicitly.

Risk: Third-party proxies may expose credentials or authenticated URLs.

Mitigation: Use third-party proxies only for public URLs without secrets, and verify downloads against independently trusted hashes.

Risk: Diagnostic output or container configuration may reveal sensitive values.

Mitigation: Redact diagnostic values and keep authenticated configuration out of container images.

## Reference(s):

- [Ecosystem mirror configuration guide](references/ecosystems.md)
- [Mirror troubleshooting guide](references/troubleshoot.md)
- [CN Mirror Download on ClawHub](https://clawhub.ai/fjjzy/skills/cn-mirror-download)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

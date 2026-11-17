## Description:

Intercept and inspect AI agent HTTP/HTTPS traffic with a MITM proxy to detect and log exfiltration and injection threats in real time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shi8103312](https://clawhub.ai/user/shi8103312)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to operate or interpret ClawSec Monitor, configure proxy-based traffic inspection, inspect threat logs, and troubleshoot findings for AI agent traffic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad HTTPS interception can expose sensitive plaintext traffic and CA trust material.

Mitigation: Use only in an isolated test environment, prefer per-process CA settings over system-wide trust, and avoid routing unrelated traffic through the proxy.

Risk: The audited package is missing the implementation it instructs users to run, so CA key handling, logs, permissions, redaction, and cleanup cannot be audited from the artifact.

Mitigation: Treat installation as a security review item and do not rely on the package until the missing implementation and operational handling are audited.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shi8103312/skills/clawsec-1-0-0)
- [Publisher profile](https://clawhub.ai/user/shi8103312)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational troubleshooting steps and threat-log interpretation guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

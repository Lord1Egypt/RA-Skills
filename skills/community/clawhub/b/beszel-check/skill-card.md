## Description:

Monitor home lab servers via Beszel (PocketBase).

This skill is ready for commercial/non-commercial use.

## Publisher:

[karakuscem](https://clawhub.ai/user/karakuscem)

### License/Terms of Use:


## Use Case:

Developers, homelab operators, and infrastructure maintainers use this skill to check Beszel system status and identify containers with high CPU usage from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable Beszel credentials may be exposed through broadly inherited or logged environment variables.

Mitigation: Use a least-privilege Beszel account, scope credentials narrowly to the agent runtime, and rotate credentials after testing or suspected exposure.

Risk: Connections to an untrusted or remote Beszel instance may expose credentials or monitoring data if HTTPS is not used correctly.

Mitigation: Use this skill only with a trusted local Beszel instance unless the code and deployment are updated to enforce HTTPS transport correctly.

Risk: Documented commands source the user's shell profile before execution, which may run unrelated local configuration.

Mitigation: Run the script directly with the required environment variables instead of sourcing the full shell profile.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/karakuscem/skills/beszel-check)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-formatted terminal text with command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and Beszel connection credentials provided through environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

AgentVerif scans skill content for OWASP LLM risks, signs skill ZIPs, verifies skill certificates, and supports license revocation for controlled distribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaymizuno](https://clawhub.ai/user/shaymizuno)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use AgentVerif to scan OpenClaw skills for common LLM security issues, sign distributable ZIP archives, verify certificates, and revoke licenses when distribution must be controlled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Skill archives can be uploaded to the configured AgentVerif endpoint during scan or sign operations.

Mitigation: Review archive contents first and do not submit ZIPs containing secrets, credentials, or proprietary material unless sharing them with that endpoint is acceptable.

Risk: The sign command can modify ZIP files in place.

Mitigation: Keep a backup copy of the original archive before signing.

Risk: Fixed certification text may overstate assurance if users treat it as a fresh scan result.

Mitigation: Verify the release and review current scan output before relying on certification claims.

Risk: Unpinned installer or dependency versions can change behavior after installation.

Mitigation: Use pinned versions for the ClawHub installer and the agentverif-sign dependency in controlled environments.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/shaymizuno/skills/agentverif)
- [Publisher profile](https://clawhub.ai/user/shaymizuno)
- [AgentVerif homepage](https://agentverif.com)
- [AgentVerif documentation](https://agentverif.com/docs)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON and text responses with optional Markdown badge output and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands return process exit codes for pass, fail, and argument or dependency errors.]

## Skill Version(s):

2.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

ClawGears conducts macOS security audits for OpenClaw-based AI assistants to detect exposure risks, weak tokens, sensitive commands, and IP leaks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinhanai](https://clawhub.ai/user/jinhanai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users on macOS use ClawGears to run security checks, inspect IP exposure, generate audit reports, and apply consent-based fixes for common OpenClaw gateway and local privacy risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads sensitive local OpenClaw configuration, permission, log, process, and macOS security data.

Mitigation: Review the scripts before use, start with the read-only quick check, and treat generated reports as sensitive local security artifacts.

Risk: The IP leak check sends the user's public IP to external services and saves exposure-check results locally.

Mitigation: Run IP leak checks only after accepting that public IP disclosure and local history storage are part of the workflow.

Risk: Security evidence reports verified bugs that can miss or truncate important findings.

Mitigation: Treat reports as potentially incomplete until the listener-detection and set -e control-flow issues are fixed.

Risk: Interactive fixes can modify OpenClaw configuration, generate new tokens, restart services, and request sudo for firewall changes.

Mitigation: Approve each fix individually after reviewing the proposed change and confirm backups exist before modifying configuration.

## Reference(s):

- [ClawGears ClawHub Skill Page](https://clawhub.ai/jinhanai/skills/clawgears-securityaudit)
- [JinHanAI ClawHub Publisher Profile](https://clawhub.ai/user/jinhanai)
- [ClawGears GitHub Repository](https://github.com/JinHanAI/ClawGears)
- [OpenClaw Exposure Database](https://openclaw.allegro.earth)
- [Censys Host Search](https://search.censys.io)
- [Shodan Host Search](https://www.shodan.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands plus optional JSON or HTML audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local security findings, public IP exposure status, and suggested or interactive configuration changes.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

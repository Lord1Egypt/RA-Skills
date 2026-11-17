## Description:

Monitor and manage Bambu Lab 3D printers in your local network with real-time status, error decoding, and a web dashboard interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouzia](https://clawhub.ai/user/zhouzia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators who run local Bambu Lab printer farms use this skill to monitor printer status, inspect progress and errors, and provide concise agent summaries for voice or chat workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Printer access codes are stored locally in plaintext configuration.

Mitigation: Protect config.json with restrictive local file permissions or move printer credentials to a secret store before operational use.

Risk: Printer connections disable certificate verification.

Mitigation: Require certificate verification or certificate pinning before using this skill on networks you do not fully control.

Risk: The local dashboard and APIs do not include authentication.

Mitigation: Keep the service bound to localhost, restrict network access, and add authentication before exposing it beyond the local machine.

Risk: Printer identifiers and telemetry may appear in API or dashboard responses.

Mitigation: Avoid exposing serial numbers in agent responses and sanitize shared dashboard or API output.

Risk: Dashboard rendering may include printer-provided fields.

Mitigation: Escape or sanitize printer, task, and material fields before using live data in shared environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhouzia/skills/bambu-agent)
- [ClawHub publisher profile](https://clawhub.ai/user/zhouzia)
- [Artifact README](artifact/README.md)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, configuration, guidance, API data]

**Output Format:** [JSON API responses, brief speech text, and an HTML dashboard]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local network access to configured Bambu Lab printers and a local printer configuration file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

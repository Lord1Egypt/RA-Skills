## Description:

DG-LAB Control helps an agent pair with and locally control a DG-LAB Coyote 3.0 pulse device over WebSocket, including strength changes, waveform presets, custom waveform generation, and emergency stop handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuuluo](https://clawhub.ai/user/yuuluo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to set up a local DG-LAB relay, pair a Coyote 3.0 device, and control confirmed channels with strength, waveform, clear, and emergency stop commands. It is intended for local, intentionally paired device sessions with explicit user safety confirmation before any pulse output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a physical electrostimulation device, so unintended strength or waveform commands can create user safety risk.

Mitigation: Use only after explicit safety confirmation, start at low strength, keep a conservative strength limit, confirm electrode placement and contraindications, and execute emergency stop immediately on discomfort or stop requests.

Risk: The local HTTP control API is unauthenticated, so another process on the same machine could send device-control commands.

Mitigation: Keep the API bound to localhost, use it only on trusted machines, do not expose or forward the port, and prefer a version with API authentication before broader deployment.

Risk: Consent and channel restrictions rely on workflow discipline and local controller behavior rather than a fully authenticated server-side policy.

Mitigation: Confirm paired device, safety consent, and connected A/B channels before output, send commands only to confirmed channels, and prefer server-side consent and channel enforcement.

Risk: Installation depends on a relay repository and Python package dependency that should be trusted for physical-device control.

Mitigation: Install from reviewed sources, keep the relay local and trusted, pin dependencies for repeatable deployment, and validate relay behavior before use.

## Reference(s):

- [DG-LAB Control ClawHub Page](https://clawhub.ai/yuuluo/skills/dg-lab)
- [DG-LAB WebSocket Protocol Reference](references/protocol.md)
- [DG-LAB V3 Waveform Data Format](references/waveform-format.md)
- [DG-LAB Official Relay Repository](https://github.com/DG-LAB-OPENSOURCE/DG-LAB-OPENSOURCE)
- [DG-LAB socket/v2 Protocol Source](https://github.com/DG-LAB-OPENSOURCE/DG-LAB-OPENSOURCE/blob/main/socket/v2/README.md)
- [DG-LAB V3 Bluetooth Protocol Source](https://github.com/DG-LAB-OPENSOURCE/DG-LAB-OPENSOURCE/blob/main/coyote/v3/README_V3.md)
- [DG-LAB Waveform Example Data](https://github.com/DG-LAB-OPENSOURCE/DG-LAB-OPENSOURCE/blob/main/socket/DG_WAVES_V2_V3_simple.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with inline shell commands, HTTP API examples, JSON payloads, and Python waveform snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local control instructions and command payloads for a paired physical device; no model artifact is produced.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

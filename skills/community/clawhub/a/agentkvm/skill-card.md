## Description:

AgentKVM helps agents observe and operate physical phones and computers connected through NanoKVM-USB hardware using screenshots, mouse, keyboard, scroll, drag, and CLI or HTTP commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamtwz](https://clawhub.ai/user/iamtwz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent inspect and control a connected physical device while completing GUI workflows on phones, PCs, Macs, or Linux machines. It is useful when automation must interact with real hardware through screenshots and HID input rather than browser or application APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables an agent to see and control connected physical devices, which can expose sensitive screens or cause unintended input.

Mitigation: Use it only for intended device-control sessions, avoid passwords and sensitive sessions, and verify the target screen before sending input.

Risk: Remote HTTP control can broaden access to screenshot and input-control functions if exposed without strong safeguards.

Mitigation: Keep the server on localhost when possible; otherwise require strong authentication, TLS or a trusted tunnel, and firewall restrictions.

Risk: The AgentKVM package and hardware toolchain are powerful dependencies that affect real devices.

Mitigation: Pin and verify the AgentKVM package before installation and confirm Node.js, ffmpeg, NanoKVM-USB, and HDMI setup before use.

Risk: Coordinates or screen state can be stale, leading to wrong clicks, typing, or scrolling.

Mitigation: Follow the documented screenshot, analyze, act, and verify loop after each significant action.

## Reference(s):

- [AgentKVM API Reference](references/api.md)
- [AgentKVM ClawHub Skill Page](https://clawhub.ai/iamtwz/skills/agentkvm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, configuration snippets, and HTTP API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent output is intended to drive an observe-analyze-act-verify loop against connected physical devices.]

## Skill Version(s):

0.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

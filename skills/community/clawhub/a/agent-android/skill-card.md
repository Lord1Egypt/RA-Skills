## Description: <br>
Control Android over LAN without USB, ADB, or root. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crazytigerman](https://clawhub.ai/user/crazytigerman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to connect an agent to a user-provided Android device URL on a trusted LAN, inspect apps and UI state, and perform stepwise taps, inputs, navigation, and screenshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connecting to an untrusted or guessed Android device URL could control the wrong device. <br>
Mitigation: Use only trusted device URLs explicitly provided by the user and do not scan or guess LAN addresses. <br>
Risk: Screenshots and UI dumps can expose private app content. <br>
Mitigation: Treat UI trees and screenshots as sensitive and save raw outputs only when the user explicitly asks for files. <br>
Risk: Exposing the phone-side service outside a private LAN could allow unintended access. <br>
Mitigation: Keep the phone-side service on a trusted private LAN and do not expose it on public networks. <br>
Risk: Automation may affect sensitive apps, account settings, private content, or irreversible actions. <br>
Mitigation: Ask for confirmation before operating sensitive apps or taking irreversible actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/crazytigerman/agent-android) <br>
- [AIVane AI RPA repository](https://github.com/aivanelabs/ai-rpa) <br>
- [Smoke checklist](https://github.com/aivanelabs/ai-rpa/blob/main/skills/agent-android/references/smoke-flow.md) <br>
- [Quickstart](https://github.com/aivanelabs/ai-rpa/blob/main/docs/quickstart.md) <br>
- [Install guide](https://github.com/aivanelabs/ai-rpa/blob/main/docs/install-agent-android.md) <br>
- [Public protocol](https://github.com/aivanelabs/ai-rpa/blob/main/docs/protocol-v1.md) <br>
- [Known beta limits](https://github.com/aivanelabs/ai-rpa/blob/main/docs/known-limitations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include device-control command sequences and optional screenshot or UI dump file paths only when requested by the user.] <br>

## Skill Version(s): <br>
0.1.6 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

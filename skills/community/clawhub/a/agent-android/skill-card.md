## Description:

Control Android over LAN without USB, ADB, or root.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crazytigerman](https://clawhub.ai/user/crazytigerman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect to a trusted Android device on the same LAN, inspect apps and UI state, and drive step-by-step tap, input, navigation, and screenshot workflows without USB, ADB, or root.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and control an Android device over unauthenticated plaintext LAN HTTP.

Mitigation: Use only a trusted device URL provided by the user, keep the phone service off public or shared Wi-Fi, and prefer an isolated trusted network or encrypted tunnel.

Risk: UI trees and screenshots can expose private app content.

Mitigation: Use a test device or non-sensitive apps when possible, ask for confirmation before sensitive or irreversible actions, and save screenshots or raw UI dumps only when explicitly requested.

Risk: The uv-installed dependency is not version-pinned in the skill metadata.

Mitigation: Review the upstream package before installation and confirm the installed package version is acceptable for the deployment.

## Reference(s):

- [Project homepage](https://github.com/aivanelabs/ai-rpa)
- [Smoke checklist](https://github.com/aivanelabs/ai-rpa/blob/main/skills/agent-android/references/smoke-flow.md)
- [Quickstart](https://github.com/aivanelabs/ai-rpa/blob/main/docs/quickstart.md)
- [Install guide](https://github.com/aivanelabs/ai-rpa/blob/main/docs/install-agent-android.md)
- [Public protocol](https://github.com/aivanelabs/ai-rpa/blob/main/docs/protocol-v1.md)
- [Known beta limits](https://github.com/aivanelabs/ai-rpa/blob/main/docs/known-limitations.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include user-approved Android control commands, trusted device URL placeholders, and screenshot file paths when explicitly requested.]

## Skill Version(s):

0.1.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

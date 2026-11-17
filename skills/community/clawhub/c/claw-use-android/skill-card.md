## Description:

Enables an AI agent to control and interact with real Android phones through a companion app and CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[4ier](https://clawhub.ai/user/4ier)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation operators use this skill to let an agent observe Android screens, execute phone actions, manage device I/O, and run reusable mobile automation flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants broad control over a real Android device, including sensitive device I/O and phone actions.

Mitigation: Install only on a dedicated test phone, isolate it on a trusted network, and avoid granting unnecessary permissions.

Risk: The security evidence flags unsafe update, permission, unlock, and cleartext network-control patterns.

Mitigation: Avoid storing a real lockscreen PIN when possible and review all device permissions before use.

Risk: The LAN HTTP APK update flow can expose users to untrusted application updates.

Mitigation: Use that update path only after independently verifying the APK source, hash, package name, and signing identity.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/4ier/skills/claw-use-android)
- [Publisher profile](https://clawhub.ai/user/4ier)
- [Skill documentation](artifact/SKILL.md)
- [Learned flows](artifact/flows.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON action payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include reusable flow definitions for Android automation tasks.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

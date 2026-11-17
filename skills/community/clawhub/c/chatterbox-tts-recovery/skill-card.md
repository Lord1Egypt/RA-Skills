## Description:

Restore and verify the Chatterbox TTS browser/OpenAI-compatible bridge stack after upgrades, reinstalls, or damaged local state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pinguy](https://clawhub.ai/user/pinguy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to recover a local Chatterbox TTS browser, Voice Lab, and OpenAI-compatible bridge installation while preserving user voices, service overrides, and local configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recovery flow may run a mutable external installer that enables user-level services without a pinned or verified source revision.

Mitigation: Use an exact trusted repository URL and a reviewed commit or signed release, inspect the installer, and run the source validation step before installation.

Risk: Recovery actions can affect user voice libraries, systemd drop-ins, default voice settings, and local overrides.

Mitigation: Back up voices and user systemd drop-ins, record custom environment variables and ports, and prefer repairing the smallest broken layer.

Risk: Changing bind addresses or using a development API key can expose local TTS services beyond the intended loopback-only posture.

Mitigation: Keep services bound to loopback unless authentication has been intentionally hardened, and replace development credentials before any broader exposure.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/pinguy/Skills/tree/main/skills/chatterbox-tts-recovery)
- [ClawHub skill page](https://clawhub.ai/pinguy/skills/chatterbox-tts-recovery)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and local service checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on inspection, state protection, targeted repair, configuration restoration, and acceptance checks.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

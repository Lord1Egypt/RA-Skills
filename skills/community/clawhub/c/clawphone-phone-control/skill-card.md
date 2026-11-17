## Description:

ClawPhone Phone Control guides agents to inspect and operate a connected phone UI through screen-state checks, app launch, control clicks, text entry, and failure recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[be1human](https://clawhub.ai/user/be1human)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide an agent through cautious, user-directed phone UI automation, especially when reading current phone state, launching apps, handling popups, clicking controls, entering text, and troubleshooting failed automation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to inspect and operate visible phone screens, which may expose sensitive messages, passwords, or one-time codes.

Mitigation: Use it only for intended phone-control sessions and avoid sensitive screens unless the user explicitly accepts visible-screen processing.

Risk: Text entry may rely on clipboard-based fallback behavior.

Mitigation: Avoid entering passwords, one-time codes, or sensitive messages through this workflow unless clipboard exposure is acceptable.

Risk: Coordinates can become invalid when the device, page, keyboard, or toolbar state changes.

Mitigation: Base coordinate actions on the current screenshot only and recheck the screen after each fragile UI operation.

## Reference(s):

- [MCP Tool Reference](artifact/tools-reference.md)
- [ClawHub skill page](https://clawhub.ai/be1human/skills/clawphone-phone-control)

## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown guidance with inline tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance emphasizes checking current screen state before actions and revalidating after fragile UI operations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

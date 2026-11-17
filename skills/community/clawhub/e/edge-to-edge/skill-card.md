## Description:

Use this skill to migrate Jetpack Compose apps to adaptive edge-to-edge support, fix UI components obscured by system bars or IME insets, and improve system bar legibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to update Android Jetpack Compose apps for edge-to-edge behavior across Activities, lists, FABs, dialogs, system bars, and soft keyboard insets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to change Android target SDK, Activity setup, manifest soft-input behavior, and Compose inset handling, which may affect layout or runtime behavior across devices.

Mitigation: Review generated AndroidManifest.xml, Activity, Gradle, and Compose layout changes before merging, and run the app build and UI checks on representative devices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ntriq-gh/skills/edge-to-edge)
- [ClawHub publisher profile](https://clawhub.ai/user/ntriq-gh)

## Skill Output:

**Output Type(s):** [Analysis, Code, Configuration instructions, Shell commands, Guidance]

**Output Format:** [Markdown with Kotlin code blocks and checklist guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose edits to Android Activity code, AndroidManifest.xml, Compose layout modifiers, and Gradle target SDK configuration.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Record and narrate a polished demo video of a web app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orrrge](https://clawhub.ai/user/orrrge)

### License/Terms of Use:

MIT

## Use Case:

Developers and product teams use this skill to create repeatable walkthroughs, feature tours, and narrated screencasts of web apps. A Python story describes what to show, and the skill produces and checks the video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser containment may be reduced.

Mitigation: Run recordings in a dedicated environment without sensitive browser profiles or data.

Risk: A recording could capture a live service or real data.

Mitigation: Use an isolated demo instance with its own port and data directory; stop if the app cannot be isolated.

Risk: Saved API keys may not be reliably protected.

Mitigation: Avoid saving keys in skill files or story files; use a short-lived credential only when a remote narration service is needed.

Risk: Some files were only partially analyzed by the security scan.

Mitigation: Review the remaining partially analyzed files before installing or relying on the skill.

## Reference(s):

- [Director reference](references/director.md)
- [Narration and speech engines](references/engines.md)
- [Narration workflow](references/narration.md)
- [Environment and installation](references/environment.md)
- [Interactive demo](https://orrrge.github.io/autoRecording/)
- [ClawHub release page](https://clawhub.ai/orrrge/skills/auto-demo-recording)

## Skill Output:

**Output Type(s):** [Video files, Code, Shell commands, Verification reports]

**Output Format:** [MP4 video, Python story files, and JSON timeline and check reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Videos are rendered at 1920×1080 and 60 fps; narration is optional.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

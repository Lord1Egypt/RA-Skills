## Description:

Controls an Android phone by using screen observations and a configured vision-language model to plan and execute app launch, tapping, swiping, text input, waiting, and task status actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liseng1997](https://clawhub.ai/user/liseng1997)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and automation operators use this skill when they want an agent to operate a connected Android phone for cross-app tasks, including opening apps, finding contacts or UI elements, entering text, and confirming task completion from screen feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a real Android phone through taps, swipes, app launches, text entry, and key presses.

Mitigation: Install it only when intentional phone control is desired, and supervise or gate actions that could affect accounts, messages, purchases, or settings.

Risk: Screenshots and task goals are sent to a configurable VLM service and may include sensitive notifications, apps, messages, or account information.

Mitigation: Use a trusted local or HTTPS VLM endpoint and avoid displaying sensitive content during automation.

Risk: Temporary screenshot files may remain on disk after visual analysis.

Mitigation: Clean up retained screenshot files after use and prefer an isolated environment for installation and execution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/liseng1997/skills/android-auto-controller)
- [ClawHub publisher profile](https://clawhub.ai/user/liseng1997)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a USB-connected Android device, Python 3, uiautomator2, OpenAI client configuration, and VLM environment variables; actions may create temporary screenshot files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

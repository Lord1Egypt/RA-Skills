## Description: <br>
Controls an Android phone with visual state analysis, popup handling, simulated taps and text entry, and screen-feedback checks for action verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liseng1997](https://clawhub.ai/user/liseng1997) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to inspect and control a connected Android device through VLM-guided commands for app navigation, popup handling, scrolling, tapping, and text entry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can broadly control a connected Android phone. <br>
Mitigation: Install only after review, use a test phone or non-sensitive profile, and personally confirm sends, purchases, or account changes. <br>
Risk: Screenshots are sent to a configurable VLM endpoint. <br>
Mitigation: Prefer a trusted local VLM endpoint and avoid displaying banking data, passwords, one-time codes, private chats, or work data. <br>
Risk: USB debugging and the ATX automation service can remain enabled after use. <br>
Mitigation: Disable USB debugging or remove ATX when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liseng1997/android-auto-controller) <br>
- [Publisher profile](https://clawhub.ai/user/liseng1997) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Android automation script](artifact/scripts/android_agent.py) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown instructions with bash command patterns and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, uiautomator2, a connected Android device with USB debugging, and VLM environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

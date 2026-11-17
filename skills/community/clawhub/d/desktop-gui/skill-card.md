## Description:

Full desktop GUI automation using Python libraries, xdotool, and scrot for mouse and keyboard simulation, screenshots, and visual recognition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baimaxx](https://clawhub.ai/user/baimaxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to control desktop applications, capture screens, locate visual elements, run OCR, and coordinate cross-application workflows when direct APIs are unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automate mouse and keyboard actions against a real desktop, which may trigger unintended clicks, text entry, or window changes.

Mitigation: Run it in an isolated desktop or virtual machine first, enable pyautogui FAILSAFE, add pauses, and require confirmation before destructive or irreversible actions.

Risk: Full desktop screenshots may contain sensitive data and the evidence reports a hard-coded plaintext HTTP vision endpoint.

Mitigation: Use a trusted HTTPS or local model endpoint configured by the user, crop or redact screenshots before sending them, and delete temporary screenshot files after use.

Risk: Unpinned Python and system dependencies may change behavior or increase supply-chain exposure.

Mitigation: Install dependencies in an isolated environment and pin package versions before repeated or sensitive use.

## Reference(s):

- [Desktop Gui ClawHub page](https://clawhub.ai/baimaxx/skills/desktop-gui)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces executable desktop automation examples and operational guidance; actions may affect the active desktop session.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

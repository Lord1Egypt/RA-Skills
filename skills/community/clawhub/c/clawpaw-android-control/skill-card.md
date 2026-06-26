## Description: <br>
Turns an Android phone into an OpenClaw-controlled node for remote UI automation, device queries, screenshots, layout retrieval, and app launching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[klscool](https://clawhub.ai/user/klscool) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to connect an Android 10+ device as a controllable node and automate phone interactions through Gateway or HTTP workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over an Android phone, including taps, swipes, text input, screenshots, app launches, and settings-affecting commands. <br>
Mitigation: Install only when phone automation is intended, keep the device supervised, and review high-impact actions before execution. <br>
Risk: Optional permissions can expose sensitive data such as location, notifications, contacts, photos, calendar entries, SMS, phone calls, and files. <br>
Mitigation: Grant only the minimum Android permissions needed for the task and avoid SMS, call, storage, contact, and photo permissions unless specifically required. <br>
Risk: HTTP control can expose device actions or data if reachable from an untrusted network. <br>
Mitigation: Keep HTTP access on a private trusted network or tunnel and avoid exposing the control port publicly. <br>
Risk: Vision analysis may send screenshots or screen-derived data to a configured external provider. <br>
Mitigation: Leave vision analysis disabled unless the provider is trusted and the screen content is appropriate to share. <br>


## Reference(s): <br>
- [ClawPaw App](https://github.com/klscool/ClawPaw) <br>
- [ClawPaw App Releases](https://github.com/klscool/ClawPaw/releases) <br>
- [OpenClaw Docs](https://docs.openclaw.ai) <br>
- [Operation Guide Index](references/INDEX.md) <br>
- [Permissions Documentation](README_PERMISSIONS.md) <br>
- [Basic Integration Example](references/guides/basic-example.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Text, Code] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON command parameters, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return JSON device responses, XML layouts, screenshots, photos, and other permission-gated phone data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

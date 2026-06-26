## Description: <br>
Audio Announcement gives OpenClaw agents real-time spoken status updates using text-to-speech, with multilingual and cross-platform support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wililam](https://clawhub.ai/user/wililam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to make agents announce received requests, task progress, completions, and errors through local audio playback. It is intended for workflows where audible status updates improve transparency without requiring the user to watch logs continuously. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spoken announcement text may be sent to an external text-to-speech service. <br>
Mitigation: Use only non-sensitive summaries in announcements, and do not announce secrets, prompts, filenames, or private task details. <br>
Risk: Startup hooks and always-on announcement behavior can create persistence the user did not intend. <br>
Mitigation: Add shell profile or session startup hooks only after explicit opt-in, and review or remove them when automatic audio status updates are no longer wanted. <br>
Risk: The workflow helper includes eval-based command execution that is unsafe with untrusted input. <br>
Mitigation: Do not pass untrusted strings to the helper; prefer direct command invocation or audit each command before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wililam/audio-announcement) <br>
- [README](README.md) <br>
- [Announcement anti-forgetting guide](docs/announcement-anti-forgetting.md) <br>
- [Microsoft text-to-speech language support](https://learn.microsoft.com/azure/ai-services/speech-service/language-support#text-to-speech) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; runtime scripts produce local spoken audio.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Announcements are short text strings converted to audio; users should avoid sensitive content in spoken messages.] <br>

## Skill Version(s): <br>
2.0.8 (source: server release metadata, package.json, setup.py, version.txt) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

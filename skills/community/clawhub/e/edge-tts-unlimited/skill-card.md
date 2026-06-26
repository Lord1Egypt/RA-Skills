## Description: <br>
Edge Tts Unlimited generates long-form audio, podcasts, voice notes, and spoken briefs with Microsoft Edge neural voices through Python edge-tts without API keys, credits, or character limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dannyshmueli](https://clawhub.ai/user/dannyshmueli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content teams, and agents use this skill to turn text or script files into MP3 spoken content for briefs, voice notes, podcasts, and long-form audio in headless or server-side environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Runtime Python package installation may fetch edge-tts through uv or pip when the dependency is not already installed. <br>
Mitigation: Review dependency policy before use, allow or pin the edge-tts package in controlled environments, and run the script where package installation is permitted. <br>
Risk: Input text may be sent to an external text-to-speech service during audio generation. <br>
Mitigation: Do not submit secrets, private documents, regulated data, or proprietary text unless policy allows that content to leave the machine. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown instructions with bash commands; runtime output is an MP3 audio file path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports direct text, file input, voice selection, speaking-rate adjustment, voice presets, and voice listing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

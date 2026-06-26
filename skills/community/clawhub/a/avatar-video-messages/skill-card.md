## Description: <br>
Generate and send video messages with a lip-syncing VRM avatar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thewulf7](https://clawhub.ai/user/thewulf7) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to turn text or audio into short avatar videos and send them as Telegram video notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send generated video notes through Telegram. <br>
Mitigation: Review the message content and destination before asking the agent to send. <br>
Risk: The workflow depends on the external avatarcam package and ffmpeg binary. <br>
Mitigation: Verify the avatarcam npm package name and publisher before installation, and install ffmpeg from a trusted package source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thewulf7/avatar-video-messages) <br>
- [Publisher profile](https://clawhub.ai/user/thewulf7) <br>
- [Avatarcam npm package](https://www.npmjs.com/package/@thewulf7/openclaw-avatarcam) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text, Video files, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and OpenClaw tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or sends MP4 avatar videos as Telegram video notes; requires avatarcam and ffmpeg.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

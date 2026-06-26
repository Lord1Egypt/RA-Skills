## Description: <br>
Feishu Mood Music recognizes emotional cues, generates matching healing or companion music, and delivers the audio to a Feishu group. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kylinr](https://clawhub.ai/user/kylinr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Feishu workspace users and bot operators use this skill to respond to mood or music requests with generated music and Feishu audio delivery. It is intended for chat-based emotional companionship, not clinical or mental-health advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend MiniMax quota and use Feishu credentials to upload and post audio. <br>
Mitigation: Use a dedicated least-privilege Feishu app, restrict allowed chat IDs, monitor quota use, and keep credentials scoped to this workflow. <br>
Risk: Implicit emotion triggers and local autoplay can generate or send audio without enough user control. <br>
Mitigation: Require confirmation for implicit triggers and local autoplay, and keep automatic posting limited to trusted users and approved chats. <br>
Risk: Mood-history logging can capture sensitive emotional context. <br>
Mitigation: Leave mood-history logging disabled unless users explicitly agree and have a clear way to delete the record. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kylinr/feishu-mood-music) <br>
- [MiniMax CLI](https://github.com/MiniMax-AI/cli) <br>
- [MiniMax Token Plan](https://platform.minimax.io/subscribe/token-plan) <br>
- [MiniMax Music Generation API](https://api.minimaxi.com/v1/music_generation) <br>
- [Feishu file upload API](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu message send API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls, Files] <br>
**Output Format:** [Markdown guidance with shell commands, generated MP3 files, and Feishu audio-message delivery.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MiniMax quota and API authentication plus Feishu app credentials for delivery.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

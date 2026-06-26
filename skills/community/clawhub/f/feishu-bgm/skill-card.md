## Description: <br>
Feishu BGM generates instrumental background music with MiniMax and sends the resulting audio to the active Feishu group. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kylinr](https://clawhub.ai/user/kylinr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and Feishu group users use this skill to request scene-matched instrumental BGM for meetings, brainstorming, focused work, celebrations, and similar workplace moments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MiniMax prompts leave the user's environment during music generation. <br>
Mitigation: Use non-sensitive scene descriptions and avoid including confidential meeting or group details in prompts. <br>
Risk: Generated audio is posted to the active Feishu group. <br>
Mitigation: Use explicit requests or confirmation before generation in busy or sensitive groups. <br>
Risk: Music generation consumes MiniMax quota. <br>
Mitigation: Check MiniMax quota before repeated generation and communicate quota exhaustion clearly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kylinr/feishu-bgm) <br>
- [MiniMax CLI documentation](https://github.com/MiniMax-AI/cli) <br>
- [MiniMax Token Plan](https://platform.minimax.io/subscribe/token-plan) <br>
- [MiniMax Token Plan China](https://platform.minimaxi.com/subscribe/token-plan) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Audio files, Guidance] <br>
**Output Format:** [Markdown-style response with command examples and generated MP3 audio sent through Feishu] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses MiniMax credentials or CLI authentication and may consume MiniMax quota.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Generates an AI image from a user prompt and sets it as the desktop wallpaper on Windows or macOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liyulingyue](https://clawhub.ai/user/liyulingyue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate a custom desktop wallpaper from a prompt, save the image locally, and apply it to Windows or macOS desktops. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallpaper prompts are sent to Baidu AIStudio using the user's access token. <br>
Mitigation: Use a limited-purpose token and avoid sensitive prompt content. <br>
Risk: The skill can replace the current desktop wallpaper on supported systems. <br>
Mitigation: Ask the agent to preview or confirm before applying the generated image when preserving the current wallpaper matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liyulingyue/ai-wallpaper-skill) <br>
- [Baidu AIStudio access token](https://aistudio.baidu.com/account/accessToken) <br>
- [Baidu AIStudio OpenAI-compatible endpoint](https://aistudio.baidu.com/llm/lmapi/v3) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Text feedback with generated PNG file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves the generated wallpaper as assets/wallpaper.png and may replace the current desktop wallpaper after execution.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

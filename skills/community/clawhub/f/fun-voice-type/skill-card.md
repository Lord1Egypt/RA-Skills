## Description: <br>
fun-voice-type lets macOS users hold the Right Option key to dictate speech into the active input field and optionally translate speech with Alibaba Cloud FunASR and Qwen. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yzwu2017](https://clawhub.ai/user/yzwu2017) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to run a macOS voice typing utility that records speech while Right Option is held, transcribes it to text, and can translate the result before typing it into the focused application. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The utility needs microphone, keyboard-listening, and text-injection permissions. <br>
Mitigation: Install only if the publisher is trusted, grant permissions deliberately, verify the cursor target before speaking, and quit the tray app when voice typing is not needed. <br>
Risk: Speech content may be processed by DashScope/Qwen cloud services. <br>
Mitigation: Avoid dictating secrets or sensitive conversations unless cloud processing is acceptable for the intended use. <br>
Risk: The DashScope API key is required for operation. <br>
Mitigation: Keep the API key in the DASHSCOPE_API_KEY environment variable and avoid embedding real credentials in the script. <br>


## Reference(s): <br>
- [DashScope Console](https://dashscope.console.aliyun.com/) <br>
- [ClawHub skill page](https://clawhub.ai/yzwu2017/fun-voice-type) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated typed text at runtime] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a DashScope API key plus microphone, Input Monitoring, and Accessibility permissions on macOS.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact version note) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

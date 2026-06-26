## Description: <br>
颜色选择与转换工具，帮助代理处理基础颜色格式识别与转换，并指导用户运行随附的本地 Python 辅助脚本。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and agents use this skill to parse common web color values, convert supported formats, and produce local command examples for color conversion workflows. It is best suited for lightweight color assistance where Python standard-library execution is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented feature set is broader than the current packaged script, so palette, gradient, or some format-specific commands may not work as described. <br>
Mitigation: Verify required commands against the packaged script before relying on them, and prefer the confirmed basic HEX parsing path unless additional behavior is tested. <br>
Risk: Unsupported or malformed color input can produce an error response instead of a conversion. <br>
Mitigation: Validate color values before passing them to the script and handle JSON error responses in the agent workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-color-picker) <br>
- [Packaged skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON or text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local Python standard-library helper script; no API key is required by the artifact.] <br>

## Skill Version(s): <br>
1.2.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

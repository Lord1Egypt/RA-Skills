## Description: <br>
Provides a DeepSeek-named OpenClaw tool scaffold that currently accepts prompts and returns placeholder responses for chat, code generation, planning, and analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[barisoezcan1905](https://clawhub.ai/user/barisoezcan1905) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers can use this skill as a placeholder interface while preparing an OpenClaw agent integration for DeepSeek-style prompt handling, code generation, problem solving, planning, and analysis. Verify functionality before relying on it for real DeepSeek API responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The current release is a placeholder and does not perform real DeepSeek API calls. <br>
Mitigation: Verify the implementation before using it in workflows that require actual DeepSeek model responses. <br>
Risk: A future version that adds real API calls may send prompts, code, and related context to DeepSeek. <br>
Mitigation: Avoid sending secrets or sensitive material unless that external processing is acceptable for the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/barisoezcan1905/deepseek) <br>
- [Publisher profile](https://clawhub.ai/user/barisoezcan1905) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [Artifact skill manifest](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [JSON result object with status, message, and prompt data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Current implementation echoes the prompt instead of performing a live DeepSeek API call.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Reduces repeated Feishu bot status checks by applying a local OpenClaw patch that caches the Feishu probe result for two hours. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bryan-chx](https://clawhub.ai/user/bryan-chx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill when Feishu gateway health checks are consuming API quota too frequently and they want a local patch that reduces repeated probe calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The patch asks for sudo and overwrites OpenClaw's Feishu probe file. <br>
Mitigation: Review the script before use, keep the generated backup, and apply it only in a disposable or backed-up OpenClaw environment. <br>
Risk: The rewritten probe reports success without preserving real Feishu health or credential failure states. <br>
Mitigation: Prefer an official fix or a patch that caches the actual probe result and preserves failure responses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bryan-chx/feishu-api-cache-fix) <br>
- [Publisher profile](https://clawhub.ai/user/bryan-chx) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash command and shell script behavior] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Applies a local file rewrite and creates a backup of the target probe file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Agent Optimizer.Skip is a lightweight agent performance optimization skill for trajectory analysis, reward feedback, prompt version tracking, A/B testing, and performance reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huang-shao](https://clawhub.ai/user/huang-shao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add local trajectory logging, reward feedback, prompt version management, A/B testing, and performance or ROI reporting to agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist raw agent task, output, reward, prompt, and report data that may contain secrets or regulated information. <br>
Mitigation: Avoid logging secrets or regulated data, redact sensitive fields before persistence, and define retention or cleanup for trajectory, reward, report, and prompt files. <br>
Risk: Agent IDs are used in local file paths without safe path constraints. <br>
Mitigation: Use only simple trusted agent IDs and add path validation before deploying the skill in shared or production workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huang-shao/agent-optimizer-skip) <br>
- [OpenClaw project homepage](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with Python snippets, shell commands, JSON configuration examples, and local JSON or JSONL report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill uses python3 and writes local trajectory, reward, prompt, and optimization report files under agent-specific optimizer directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

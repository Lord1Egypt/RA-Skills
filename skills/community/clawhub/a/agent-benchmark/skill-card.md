## Description: <br>
Agent Benchmark evaluates AI agents with standardized tasks across file operations, data processing, system operations, robustness, and code quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent evaluators use this skill to run lightweight benchmark tasks, score task completion, and generate Markdown reports for comparing or diagnosing AI agent behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task files are executed as local code with broad access to files and environment variables. <br>
Mitigation: Use only trusted task sets, run in a disposable or sandboxed workspace, and clear sensitive environment variables before execution. <br>
Risk: Benchmark output can be written outside the skill directory through the memory-report behavior. <br>
Mitigation: Review or disable memory-report writing before running on machines with secrets or important files. <br>
Risk: Task path handling and generated report files can affect local workspace contents. <br>
Mitigation: Run from a controlled workspace and review task file paths and output paths before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yuyonghao-123/agent-benchmark) <br>
- [Publisher Profile](https://clawhub.ai/user/yuyonghao-123) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown benchmark reports, task result summaries, and executable task definitions/scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can execute local task code and write benchmark report files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata, target metadata, package.json, and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

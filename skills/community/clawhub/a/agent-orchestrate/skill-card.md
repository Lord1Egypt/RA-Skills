## Description: <br>
Agent Orchestrate is a quick reference for OpenClaw multi-agent orchestration patterns, including sub-agent spawning, parallel fan-out, pipelines, dependency trees, and supervision. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moltenbot000](https://clawhub.ai/user/moltenbot000) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to choose and apply simple OpenClaw multi-agent coordination patterns for parallel research, sequential pipelines, dependency-managed work, and human checkpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fan-out and synthesis patterns can expose secrets, credentials, personal data, or regulated material to additional sub-agents. <br>
Mitigation: Scope each sub-agent prompt to the minimum necessary context and avoid delegating sensitive material unless it is required for the task. <br>
Risk: Parallel or dependency-based workflows can produce partial, failed, or stale subtask results that affect final synthesis. <br>
Mitigation: Use clear labels, timeouts, checkpoints, failure handling, and human review before relying on aggregated results. <br>


## Reference(s): <br>
- [Fan-Out Pattern](references/fan-out.md) <br>
- [Pipeline Pattern](references/pipeline.md) <br>
- [Dependency Tree Pattern](references/dependency-tree.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands] <br>
**Output Format:** [Markdown with inline code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides orchestration patterns, examples, and operational cautions rather than executable automation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

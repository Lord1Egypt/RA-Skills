## Description: <br>
Master-Worker Agent Cluster for parallel task execution. Use when building distributed agent systems with parallel processing needs, task orchestration, or MapReduce-style workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gl813788-byte](https://clawhub.ai/user/gl813788-byte) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use Agent Weave to build master-worker agent clusters that execute tasks in parallel, coordinate worker agents, and support MapReduce-style workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaged npm bin metadata appears inconsistent with the artifact files. <br>
Mitigation: Verify the package contents and CLI entry point before installation or execution. <br>
Risk: Task functions executed by worker agents can run local code supplied to the orchestration framework. <br>
Mitigation: Run only trusted task functions and prefer project-local installation. <br>
Risk: Large worker counts or long-running tasks can consume local compute resources. <br>
Mitigation: Set practical worker-count and timeout limits for expensive jobs. <br>
Risk: Generated ./agent-logs files may contain sensitive local task data. <br>
Mitigation: Review, protect, and clean local log files according to the deployment environment's data-handling requirements. <br>


## Reference(s): <br>
- [Agent Weave ClawHub Page](https://clawhub.ai/gl813788-byte/agent-weave) <br>
- [README](artifact/README.md) <br>
- [Skill Documentation](artifact/SKILL.md) <br>
- [Test Report](artifact/TEST_REPORT.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports local Node.js usage, CLI workflows, and generated task orchestration patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

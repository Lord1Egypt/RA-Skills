## Description: <br>
Benchmark your OpenClaw agent across 40 real-world tasks covering file creation, research, data analysis, multi-step workflows, memory, error handling, and tool efficiency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Exe215](https://clawhub.ai/user/Exe215) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use AgentBench to run a structured benchmark suite against an OpenClaw agent, then review scores, metrics, reports, and domain-level performance results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The benchmark creates many local files and per-task workspaces while running. <br>
Mitigation: Run AgentBench from an isolated workspace and inspect generated files before retaining or sharing them. <br>
Risk: Task setup scripts may initialize repositories or modify temporary task directories. <br>
Mitigation: Use the documented /benchmark commands and do not manually point setup.sh scripts at an existing project, home directory, or sensitive path. <br>
Risk: Benchmark result files may contain details about the agent run before submission to the leaderboard. <br>
Mitigation: Review results.json, report.md, and report.html before uploading or sharing benchmark results. <br>


## Reference(s): <br>
- [AgentBench ClawHub listing](https://clawhub.ai/Exe215/agentbench) <br>
- [AgentBench homepage](https://www.agentbench.app) <br>
- [AgentBench leaderboard](https://www.agentbench.app/leaderboard) <br>
- [AgentBench result submission](https://www.agentbench.app/submit) <br>
- [Claude Code version referenced by README](https://github.com/agentbench/agentbench) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, HTML, Shell commands, Files, Guidance] <br>
**Output Format:** [Console status text plus local Markdown, HTML, and JSON result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates an agentbench-results/{run-id}/ directory containing report.md, report.html, results.json, per-task scores, metrics, and copied task outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

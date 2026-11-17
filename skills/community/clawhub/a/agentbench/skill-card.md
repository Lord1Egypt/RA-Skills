## Description:

Benchmark OpenClaw agents across 40 real-world tasks covering file creation, research, data analysis, multi-step workflows, memory, error handling, and tool efficiency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[exe215](https://clawhub.ai/user/exe215)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use AgentBench to run a local benchmark suite for OpenClaw agents and compare performance across task domains. The skill produces run reports, metrics, and leaderboard-ready result data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The benchmark executes bundled local setup scripts during task runs.

Mitigation: Run the benchmark in an isolated workspace or disposable environment before trusting results or generated files.

Risk: One memory task may write package-authored preferences into the agent's persistent memory.

Mitigation: Skip or manually reset the persistent-memory task when testing an agent profile that contains real user preferences.

Risk: The generated signature and externally verified label should not be treated as independent proof of result integrity.

Mitigation: Treat submitted results as benchmark metadata unless they have been reviewed through a separate trusted verification process.

## Reference(s):

- [AgentBench ClawHub Skill Page](https://clawhub.ai/exe215/skills/agentbench)
- [AgentBench Homepage](https://www.agentbench.app)
- [AgentBench Leaderboard](https://www.agentbench.app/leaderboard)
- [AgentBench Results Submission](https://www.agentbench.app/submit)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, HTML, Files, Shell commands]

**Output Format:** [Markdown status output plus JSON, Markdown, and HTML result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates agentbench-results/{run-id}/ with results.json, report.md, report.html, per-task scores, and metrics; requires jq, bash, and python3.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

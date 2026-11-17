## Description:

Use when the user wants to monitor how ChatGPT, Claude, Gemini, and other LLMs describe a developer tool, API, SDK, or open-source project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veeicwgy](https://clawhub.ai/user/veeicwgy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, open-source maintainers, API teams, SDK teams, and DevRel teams use this skill to design query pools, monitor model answers, score visibility metrics, diagnose inaccurate or negative claims, and plan T+7 or T+14 repair validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API collection mode can expose provider keys, endpoint choices, or sensitive query text if configured carelessly.

Mitigation: Prefer quickstart replay or manual paste mode for local-only evaluation; for API collection, keep keys in environment variables, verify OPENAI_BASE_URL, and avoid confidential query text.

Risk: Local installation and runner scripts can introduce ordinary dependency and execution risk.

Mitigation: Review install.sh, quickstart.sh, and selected runner scripts before execution, and consider pinning dependencies or using an isolated environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/veeicwgy/skills/devtool-answer-monitor)
- [DevTool Answer Monitor repository](https://github.com/veeicwgy/devtool-answer-monitor)
- [Zero-install demo viewer](https://cdn.jsdelivr.net/gh/veeicwgy/devtool-answer-monitor@main/docs/index.html)
- [MinerU public benchmark](https://github.com/veeicwgy/devtool-answer-monitor/blob/main/benchmark/mineru-public-benchmark.md)
- [Sciverse API public benchmark](https://github.com/veeicwgy/devtool-answer-monitor/blob/main/benchmark/sciverse-api-public-benchmark.md)
- [Metric definition](docs/metric-definition.md)
- [Getting started](docs/getting-started.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON artifacts, shell commands, report outlines, score drafts, and repair plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include query pools, monitoring summaries, score tables, action backlogs, weekly reports, and T+7 or T+14 regression validation plans.]

## Skill Version(s):

0.3.0 (source: server release evidence and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

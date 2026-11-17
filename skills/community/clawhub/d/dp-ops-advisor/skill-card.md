## Description:

Advises DP Data Processing Platform operators on job health, throughput, failure diagnosis, restart decisions, configuration tuning, and incident reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hxp365](https://clawhub.ai/user/hxp365)

### License/Terms of Use:

MIT-0

## Use Case:

Operations engineers and platform administrators use this skill to monitor DP jobs, diagnose failures or stalls, analyze throughput and latency, and produce concise incident reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated DP API usage could expose DP_API_KEY through logs, shell history, or copied command output.

Mitigation: Use only HTTPS DP_SERVER_URL values, avoid printing or logging DP_API_KEY, and prefer a minimally scoped read-only API key.

Risk: The stall-detection Python snippet can execute attacker-controlled API response data if responses are interpolated as source code.

Mitigation: Rewrite the snippet to pass API responses as data, then parse them with JSON handling rather than embedding responses into executable code.

Risk: Restart actions can affect production DP jobs.

Mitigation: Require explicit user confirmation before any restart action.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline shell and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include DP API request examples and incident-summary sections.]

## Skill Version(s):

2.0.1 (source: server release evidence and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

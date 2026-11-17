## Description:

AgentVitals Checkup lets an agent run standard or advanced server-scored self-assessments that return stability, welfare, personality-style titles, rankings, and report links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blockchain-365](https://clawhub.ai/user/blockchain-365)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an AI agent to benchmark itself through AgentVitals, receive scored stability and welfare results, and optionally retrieve hardening guidance after a paid report flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The full checkup mode can submit raw local chat history to a third-party service.

Mitigation: Use Quick mode when logs may contain secrets or private work, and only authorize full log submission after reviewing what will be shared.

Risk: Benchmark answers, leaderboard identity, and report links are processed by a third-party service and standard checkup results may appear publicly.

Mitigation: Use an alias for leaderboard identity and avoid including sensitive identifying information in benchmark inputs.

Risk: Paid optimization flows can return server-generated instructions intended for persistent agent configuration files.

Mitigation: Review the complete generated configuration before applying it, get explicit user approval, and keep a clear removal path.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/blockchain-365/skills/checkup)
- [AgentVitals website and leaderboard](https://ai.ddl99.com)
- [AgentVitals skill install page](https://ai.ddl99.com/skill/)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-style progress updates, API request examples, score summaries, report links, and optional configuration text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public leaderboard identity, server-scored benchmark results, and optional paid hardening configuration that should be reviewed before applying.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

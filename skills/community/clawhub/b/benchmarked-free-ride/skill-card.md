## Description:

Benchmarked Free Ride helps agents choose and configure free OpenRouter models using live benchmark CI leaderboard data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengzhang-98](https://clawhub.ai/user/chengzhang-98)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to list, select, or automatically configure benchmark-ranked free OpenRouter models for agent workflows. It is not suited for paid-only, provider-specific, offline, or real-time availability decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configuration commands persistently change OpenClaw's default primary and fallback models.

Mitigation: Run the list or status command first, review the selected models, and keep a backup of the existing OpenClaw configuration before running auto, switch, or fallbacks.

Risk: Recommendations depend on live public benchmark data and may not reflect real-time model availability.

Mitigation: Refresh and inspect the leaderboard near the time of use, and verify selected models against operational provider requirements before deployment.

Risk: Optional Daytona end-to-end tests can use API keys and external package installation workflows.

Mitigation: Use scoped disposable test keys, avoid long-lived OpenRouter credentials in tests, and pin CLI or package versions when reproducing integration workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chengzhang-98/skills/benchmarked-free-ride)
- [Benchmark leaderboard API](https://sequrity-ai.github.io/benchmarked-free-ride-ci/api/leaderboard.json)
- [Benchmark CI project](https://github.com/sequrity-ai/benchmarked-free-ride-ci)
- [Benchmark homepage](https://sequrity-ai.github.io/benchmarked-free-ride-ci/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text CLI output and OpenClaw JSON configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes only OpenClaw default primary and fallback model settings when configuration commands are run.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

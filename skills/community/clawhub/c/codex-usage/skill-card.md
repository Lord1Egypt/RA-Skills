## Description:

Manual Telegram slash-style command for Codex profile status and usage checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deadlysilent](https://clawhub.ai/user/deadlysilent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Codex users use this skill to respond to /codex_usage requests and check profile status, usage limits, and authentication health. The artifact is a deprecated wrapper that forwards requests to a separate codex-profiler implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unbundled external codex-profiler implementation.

Mitigation: Install and use it only when the paired profiler package is trusted and reviewed.

Risk: The wrapper asks the profiler to process all profiles, even when a narrower profile was requested.

Mitigation: Use only when all-profile usage and authentication-health checks are acceptable.

## Reference(s):

- [Codex Usage on ClawHub](https://clawhub.ai/deadlysilent/skills/codex-usage)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The wrapper requests all profile usage and authentication-health checks through an external codex-profiler package.]

## Skill Version(s):

1.0.19 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

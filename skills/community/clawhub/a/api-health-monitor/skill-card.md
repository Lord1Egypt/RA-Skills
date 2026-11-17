## Description:

Parses recent OpenClaw session logs for LLM API errors and returns a structured health report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toller892](https://clawhub.ai/user/toller892)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to troubleshoot LLM API health by scanning recent local OpenClaw session logs for server errors, token failures, cooldowns, rate limits, and service-busy signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads recent local OpenClaw session logs, which may contain sensitive prompts or operational details.

Mitigation: Run it deliberately for troubleshooting, avoid always-on monitoring, and review whether local logs are appropriate to inspect in the target environment.

Risk: The artifact does not add explicit file size or symlink checks before reading matching session files.

Mitigation: Use it in trusted local environments and consider adding size and symlink checks before shared or untrusted deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON object with health status, grouped errors, and a recommendation string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads recent local OpenClaw session log files and summarizes matched API error patterns.]

## Skill Version(s):

1.0.1 (source: server release metadata; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

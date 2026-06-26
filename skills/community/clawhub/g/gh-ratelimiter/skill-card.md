## Description: <br>
In-memory sliding window rate limiter for AI agents that creates per-key limits, checks quota before calls, consumes requests, resets quotas, and lists limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to run a local helper service that tracks API quotas before and after external API calls. It is intended for per-key rate-limit checks, consumption, reset, deletion, and listing during agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local service has no built-in authentication and exposes endpoints that can create, reset, or delete rate-limit entries. <br>
Mitigation: Run it only on localhost or behind trusted access controls, as recommended by the security guidance. <br>
Risk: Rate-limit state is stored in memory and is lost when the service restarts. <br>
Mitigation: Use it for local workflow coordination where ephemeral quota tracking is acceptable, or add persistent storage before relying on it for durable enforcement. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mirni/gh-ratelimiter) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, API calls, configuration, JSON] <br>
**Output Format:** [Markdown with bash and curl examples plus JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs an in-memory local service; state is not persistent across process restarts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description:

Use the arr-cli Python package to query a self-hosted media stack (Jellyfin / Radarr / Sonarr / Maintainerr / Seerr). Use it to find out what's currently playing, what's coming up, what's about to be deleted, and so on.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bottanicals](https://clawhub.ai/user/bottanicals)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use this skill to query authorized self-hosted media services for playback, queues, requests, calendars, storage, and health without mutating the stack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries can expose private media activity, requests, recent viewing, and raw service payloads.

Mitigation: Run the skill only against media stacks you operate or are authorized to inspect, and avoid logging or sharing verbose/debug output.

Risk: Maintainerr endpoints may be reachable without service-level authentication.

Mitigation: Keep Maintainerr on a trusted private network and use quiet mode in automation when the auth warning is already understood.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bottanicals/skills/arr-cli)
- [arr-cli homepage](https://github.com/BottaniCals/arr-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and CLI output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The described CLIs emit JSON or tabular stdout, with diagnostics on stderr; verbose/debug modes may expose fuller service payloads.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

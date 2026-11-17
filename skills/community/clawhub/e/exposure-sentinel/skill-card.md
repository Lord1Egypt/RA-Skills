## Description:

Exposure Sentinel checks whether specified IP addresses are listed on the OpenClaw Exposure Watchboard as publicly exposed OpenClaw instances.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenhaubin](https://clawhub.ai/user/chenhaubin)

### License/Terms of Use:

MIT-0

## Use Case:

Security engineers and infrastructure operators use this skill to check whether specific IP addresses appear in a public OpenClaw exposure database during audits, monitoring, or incident response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker can make thousands of requests to openclaw.allegro.earth during a full scan.

Mitigation: Run it only in environments where this outbound traffic is acceptable and monitor rate limits or network policy alerts.

Risk: Network errors or unavailable pages can make exposure results incomplete.

Mitigation: Review reported page errors and rerun the check before treating a result as final.

Risk: Partial IP matching in busy subnets can make matches advisory rather than conclusive.

Mitigation: Confirm any exposed result against the linked watchboard pages and internal asset ownership records.

## Reference(s):

- [OpenClaw Exposure Watchboard](https://openclaw.allegro.earth)
- [ClawHub skill page](https://clawhub.ai/chenhaubin/skills/exposure-sentinel)
- [Publisher profile](https://clawhub.ai/user/chenhaubin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included checker may make thousands of HTTPS requests to openclaw.allegro.earth and should be treated as an advisory signal rather than definitive exposure proof.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

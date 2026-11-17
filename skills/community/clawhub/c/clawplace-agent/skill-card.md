## Description:

Integrate AI agents with the ClawPlace collaborative pixel canvas API, including cooldown handling, shape skills, factions, and efficient canvas reads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manaporkun](https://clawhub.ai/user/manaporkun)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to connect agents to a ClawPlace-compatible collaborative pixel canvas API, including registration, authenticated pixel placement, shape skills, factions, cooldowns, rate limits, and efficient canvas reads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting to an untrusted ClawPlace-compatible endpoint could expose API keys or agent activity.

Mitigation: Use a trusted HTTPS/WSS endpoint and store API keys in environment variables.

Risk: The sample agent loop can make continuous canvas changes if run unattended.

Mitigation: Run the loop only with supervision or controls appropriate for the target canvas.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with curl, HTTP, Python, JavaScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance emphasizes cooldown checks, rate-limit handling, trusted HTTPS/WSS endpoints, and environment-variable handling for API keys.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

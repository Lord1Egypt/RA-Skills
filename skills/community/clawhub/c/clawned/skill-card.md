## Description:

Security agent that inventories installed OpenClaw skills, analyzes them for threats, and syncs results to your Clawned dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jenish-sojitra](https://clawhub.ai/user/jenish-sojitra)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to inventory installed skills, scan selected skill directories for security threats, and sync security status to a Clawned dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can register the host and sync installed skill metadata to the Clawned service.

Mitigation: Install only when you trust Clawned and are comfortable sharing host registration data and skill inventory metadata with the configured service.

Risk: The optional CLAWNED_SERVER setting changes the destination for authenticated API calls.

Mitigation: Use the default HTTPS endpoint or a trusted HTTPS server, and do not point CLAWNED_SERVER at untrusted or plaintext endpoints.

Risk: Daemon and watch modes can continue inspecting installed skills and syncing metadata after the original command finishes.

Mitigation: Use daemon or watch modes only when continuous monitoring is intended, and stop the daemon when ongoing sync is no longer needed.

Risk: Explicit scan commands read scannable files from the selected skill directory and send file contents for analysis.

Mitigation: Run path scans only on skill directories whose contents are acceptable to send to the configured Clawned server.

## Reference(s):

- [Clawned skill page](https://clawhub.ai/jenish-sojitra/skills/clawned)
- [Clawned homepage](https://clawned.io)
- [Threat Model - OpenClaw Skill Security](references/threat-model.md)
- [Detection Patterns - Signature Rules](references/detection-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Command-line text output, JSON for scan responses, and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and CLAWNED_API_KEY; CLAWNED_SERVER is optional.]

## Skill Version(s):

1.3.5 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

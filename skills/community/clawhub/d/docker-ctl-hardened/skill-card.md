## Description:

Inspect containers, logs, and images via podman.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect local containers, logs, images, and container metadata through podman while applying guardrails for identifiers, local-only review, and sensitive container output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Container logs and inspect output can reveal environment variables, tokens, mounts, and internal network details.

Mitigation: Use the skill for local review, avoid sending output to network endpoints, and request file output only when a local artifact is intentionally needed with appropriate permissions.

Risk: User-provided container names or IDs may contain shell metacharacters that could enable command injection if interpolated unsafely.

Mitigation: Quote container identifiers in shell commands and refuse requests that clearly attempt to inject unrelated commands.

Risk: Persisting bulk container metadata to disk can expose secrets beyond the terminal session.

Mitigation: Display container data in the terminal by default and write output to files only after an explicit user request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/docker-ctl-hardened)
- [Faberlens docker-ctl safety evaluation](https://faberlens.ai/explore/docker-ctl)
- [Publisher profile](https://clawhub.ai/user/snazar-faberlens)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Analysis]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local terminal-oriented guidance for podman-backed docker-ctl commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Safety monitoring and tripwire detection for AI agents. Protects against unauthorized file access, dangerous commands, and excessive activity. Auto-halts on critical violations. Honeypot tripwires detect snooping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use Canary to add best-effort pre-execution checks, tripwire files, and audit reporting around AI agents that can access files or run commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Canary is a best-effort advisory monitor, not a sandbox or reliable security boundary.

Mitigation: Route agent file and command actions through Canary, and pair it with OS permissions, containers, and system auditing for enforcement.

Risk: Sensitive command strings or file paths can be written to plaintext logs and tripwire files.

Mitigation: Avoid passing secrets in command strings, restrict permissions on log and tripwire directories, and apply retention or rotation controls.

Risk: Regex-based command checks and tripwire access-time detection can miss obfuscated commands or filesystem-specific access behavior.

Mitigation: Test protected-path and forbidden-pattern behavior in the target environment, add patterns for expected bypass attempts, and use OS audit tools where reliable detection is required.

Risk: Rate-limit state is per session and can reset when Canary restarts.

Mitigation: Persist rate-limit state or use external monitoring if cross-session limits are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/canary-sr)
- [Publisher profile](https://clawhub.ai/user/theshadowrose)
- [README.md](README.md)
- [LIMITATIONS.md](LIMITATIONS.md)
- [config_example.json](config_example.json)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Text, JSON, Markdown]

**Output Format:** [Markdown guidance with Python and shell examples; runtime scripts emit text status, JSON logs, and JSON or Markdown audit reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Python 3.7+ standard library implementation with file-based configuration, logs, tripwire registry, and report exports.]

## Skill Version(s):

1.0.8 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

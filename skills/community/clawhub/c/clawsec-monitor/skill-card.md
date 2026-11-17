## Description:

Clawsec Monitor helps agents configure and troubleshoot a local HTTP/HTTPS proxy that inspects AI agent traffic and logs suspected secret leakage, sensitive file access, and command injection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[funsaized](https://clawhub.ai/user/funsaized)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to set up ClawSec Monitor around AI agents, route selected agent traffic through the proxy, inspect threat logs, and troubleshoot HTTPS interception or deployment issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTTPS interception can expose decrypted agent traffic and relies on a locally trusted CA key.

Mitigation: Use per-process proxy and CA environment variables, avoid system-wide CA trust on production machines, and run with --no-mitm when decrypted HTTPS inspection is not needed.

Risk: Threat logs and snippets may contain sensitive data from intercepted requests or responses.

Mitigation: Protect access to /tmp/clawsec, review retention needs, and remove logs and CA material when monitoring is complete.

Risk: The monitor is a detection and visibility tool with known evasion and PID-handling limitations.

Mitigation: Treat findings as security signals rather than guaranteed blocking, review alerts manually, and pair the tool with other controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/funsaized/skills/clawsec-monitor)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and JSON log interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local ClawSec files such as /tmp/clawsec/threats.jsonl, proxy environment variables, and optional HTTPS CA trust settings.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

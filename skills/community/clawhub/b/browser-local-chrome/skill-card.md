## Description:

Configures and manages a local Chrome debug-mode browser for OpenClaw browser automation, including startup, status checks, OpenClaw browser configuration, troubleshooting, and shutdown guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liulike](https://clawhub.ai/user/liulike)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect OpenClaw browser automation to a locally running Chrome instance when JavaScript rendering, screenshots, page analysis, or interactive web operations are needed. It is also used as a fallback or troubleshooting path when the OpenClaw-managed browser is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill weakens browser network protections by enabling private-network access.

Mitigation: Install only in a trusted local environment, prefer a hostname allowlist over broad private-network access, and review OpenClaw browser configuration before use.

Risk: The security evidence says setup and configuration scripts can overwrite OpenClaw browser configuration.

Mitigation: Back up openclaw.json before running setup or configure scripts, and review the resulting browser profile and SSRF policy before restarting the gateway.

Risk: The security evidence says local scripts can run shell commands from unvalidated inputs and that stop-chrome.js may close unrelated Chrome sessions.

Mitigation: Do not pass untrusted port, version, or output-file arguments to the scripts, and close unrelated Chrome work before running the shutdown script.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liulike/skills/browser-local-chrome)
- [Publisher profile](https://clawhub.ai/user/liulike)
- [README.md](artifact/README.md)
- [HYBRID-MODE.md](artifact/HYBRID-MODE.md)
- [INSTALL.md](artifact/INSTALL.md)
- [QUICKSTART.md](artifact/QUICKSTART.md)
- [RELEASE.md](artifact/RELEASE.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local browser lifecycle commands, OpenClaw configuration steps, status checks, and troubleshooting guidance.]

## Skill Version(s):

1.1.0 (source: server release metadata, artifact _meta.json, RELEASE.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

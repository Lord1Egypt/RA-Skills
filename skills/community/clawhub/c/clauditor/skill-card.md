## Description:

Tamper-resistant audit watchdog for Clawdbot agents. Detects and logs suspicious filesystem activity with HMAC-chained evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apollostreetcompany](https://clawhub.ai/user/apollostreetcompany)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use Clauditor to install and operate a Linux systemd watchdog for Clawdbot activity. It monitors selected command and filesystem activity, writes tamper-evident audit logs, and produces status, digest, and alert outputs for suspicious behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release installs boot-persistent services with hidden-looking systemd names.

Mitigation: Install only on Linux hosts where this monitoring is intentional, review the service names and unit files before enabling them, and prefer transparent naming in managed environments.

Risk: Installation and privileged monitoring require root or equivalent system capabilities.

Mitigation: Build as an unprivileged user, review installer commands before running them with sudo, and restrict watch paths and target UID to the intended account.

Risk: Command details, logs, and alerts can retain or forward sensitive command-line data.

Mitigation: Treat logs and alert queues as sensitive, avoid logging full command arguments unless accepted by policy, and disable or tightly control remote and command alert channels.

## Reference(s):

- [Clauditor ClawHub Skill Page](https://clawhub.ai/apollostreetcompany/skills/clauditor)
- [Declared Project Homepage](https://github.com/apollostreetcompany/clauditor)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text guidance with inline shell commands, JSON status responses, and Markdown or JSON digest reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Linux with systemd, Cargo for building, and root-assisted installation for persistent monitoring.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

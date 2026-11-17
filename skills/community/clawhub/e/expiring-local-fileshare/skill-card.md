## Description:

Lets OpenClaw share single local workspace files through expiring, tokenized local-network HTTP links with optional one-time access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tradmangh](https://clawhub.ai/user/tradmangh)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to create short-lived local or VPN-only browser links for individual workspace files such as images, Markdown, PDFs, or text files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected workspace files are exposed over plain HTTP to local or VPN network clients that possess the generated bearer link.

Mitigation: Share only non-sensitive files, prefer short expirations and one-time links, and do not use this skill for secrets, keys, credentials, regulated data, or highly sensitive files.

Risk: Generated links and server details are written to /tmp logs, which can matter on multi-user systems.

Mitigation: Treat links as bearer credentials, review local log exposure, and remove share logs when they are no longer needed.

Risk: A background share server can continue serving until the token expires or the process is stopped.

Mitigation: Stop active share processes when finished using the printed PID or the documented kill commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tradmangh/skills/expiring-local-fileshare)
- [Publisher Profile](https://clawhub.ai/user/tradmangh)
- [Metadata Homepage](https://github.com/tradmangh)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and a local HTTP link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns one expiring tokenized URL for a single file, plus the background server PID and stop command.]

## Skill Version(s):

1.0.2 (source: evidence.release.version, artifact/METADATA.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

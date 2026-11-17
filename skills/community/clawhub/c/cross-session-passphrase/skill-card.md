## Description:

Guides cross-session communication through registered passphrases and helps users ask about activity in parallel sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

All rights reserved (documentation; MIT applies only to .py files)

## Use Case:

Users coordinating agents across sessions on the same machine and account can register passphrases to relay instructions or ask what happened in another session. Review stored instructions and obtain fresh consent before sharing file contents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent passphrase rules may prompt a later session to read or repeat a file without fresh consent.

Mitigation: Review registered instructions and require explicit approval in each session before reading or disclosing files.

Risk: Cross-session relays may expose secrets or sensitive business data.

Mitigation: Do not use passphrases to transfer credentials, private files, or sensitive business information.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/cross-session-passphrase)
- [Publisher profile](https://clawhub.ai/user/zhaoxinghua09-cell)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions]

**Output Format:** [Text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cross-session use is limited to the same machine and account.]

## Skill Version(s):

1.2.3 (source: ClawHub release metadata; bundled files state 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

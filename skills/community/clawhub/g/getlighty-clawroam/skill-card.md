## Description:

Portable identity vault for OpenClaw that syncs knowledge, packages, and memory across machines with automatic encrypted storage through user-selected providers or ClawRoam Cloud.

This skill is ready for commercial/non-commercial use.

## Publisher:

[getlighty](https://clawhub.ai/user/getlighty)

### License/Terms of Use:

MIT

## Use Case:

External OpenClaw users and developers use this skill to initialize, sync, migrate, back up, and restore an agent vault across machines while choosing managed cloud or bring-your-own storage providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad OpenClaw mirroring may expose more local agent state than intended.

Mitigation: Review the sync scope before installation and test with a non-sensitive vault until the intended include and exclude rules are confirmed.

Risk: Cloud authentication and key-enrollment behavior requires review before use with real accounts.

Mitigation: Use non-sensitive provider accounts during evaluation and review or fix the authentication and key-registration flow before production use.

Risk: Setup paths involving rclone installation, SSH host-key policy, and package-install command evaluation need review.

Mitigation: Inspect setup scripts and generated package commands before execution, and confirm SSH host-key handling before connecting to remote storage.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/getlighty/skills/getlighty-clawroam)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Per-Profile File Sync Rules Design](artifact/docs/plans/2026-02-23-file-sync-rules-design.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local sync, migration, provider setup, key management, package tracking, and status commands for the user's OpenClaw vault.]

## Skill Version(s):

2.1.1 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

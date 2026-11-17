## Description:

Back up selected local Claude and Codex session stores additively into an explicitly chosen private destination, with a no-write preview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use Amber to preview and perform authorized, local-only backups of Claude Code and Codex session stores into a private destination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups can contain private transcripts and embedded secrets even when credential filenames are excluded.

Mitigation: Keep destinations private, use encrypted storage where appropriate, and do not publish or commit raw backups.

Risk: Running the backup without review may copy unintended local session data.

Mitigation: Inspect the dry-run JSON first and run without --dry-run only after the destination and host list are authorized.

Risk: The optional npx installation path introduces network installer supply-chain risk.

Mitigation: Prefer a manual copy or reviewed local script path unless the network installer risk is accepted.

Risk: Existing backup files are preserved, so growing transcript files are not refreshed in an old destination.

Mitigation: Use a fresh private destination for each refresh when later transcript bytes must be captured.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antreasantoniou/skills/amber-agent-skill)
- [README](README.md)
- [Security and privacy](SECURITY.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run preview before writes; backup status is JSON on stdout.]

## Skill Version(s):

0.1.0 (source: changelog, released 2026-09-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

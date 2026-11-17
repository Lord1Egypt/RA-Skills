## Description:

Cursor Doctor diagnoses Cursor IDE errors, crashes, AI failures, proxy and network issues, configuration problems, and sync errors, then suggests or applies targeted fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minirr890112-byte](https://clawhub.ai/user/minirr890112-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose Cursor IDE installation, environment, and log problems, match error text to known signatures, and receive or run targeted repair commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repair actions can close Cursor, delete caches, or reset settings.

Mitigation: Run diagnosis first, save Cursor work, and apply fixes only after reviewing the intended category and expected local changes.

Risk: Proxy environment values may appear in diagnostic or repair output.

Mitigation: Redact HTTP_PROXY, HTTPS_PROXY, and related proxy values before sharing output.

Risk: Installation source clarity is limited and the security verdict requires review.

Mitigation: Install only from a verified, pinned source and review the skill before deployment.

## Reference(s):

- [Cursor Doctor GitHub homepage](https://github.com/minirr890112-byte/cursor-doctor)
- [Cursor Doctor ClawHub skill page](https://clawhub.ai/minirr890112-byte/skills/cursor-doctor)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance, Guidance]

**Output Format:** [Plain text and Markdown-style CLI guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local system, Cursor log, and proxy environment observations; repair commands can modify Cursor caches or settings.]

## Skill Version(s):

1.1.0 (source: server release evidence and SKILL.md frontmatter; pyproject.toml and package __version__ list 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

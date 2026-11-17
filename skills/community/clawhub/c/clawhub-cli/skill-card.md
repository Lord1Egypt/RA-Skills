## Description:

Use the ClawHub CLI to search, install, update, and publish agent skills from clawhub.ai.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlang-cn](https://clawhub.ai/user/openlang-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to discover, install, update, publish, and sync ClawHub skills with the npm-installed ClawHub CLI. It helps choose safe command patterns, validate publishing inputs, and troubleshoot common CLI errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A bundled bulk sync helper may run a real publish or sync when dry-run is requested but the installed CLI does not support --dry-run.

Mitigation: Verify `clawhub sync --help` before using dry-run behavior, and avoid the bundled `sync-all.sh --dry-run` path unless the local CLI explicitly supports it.

Risk: Publishing or syncing skill folders can expose secrets, private credentials, proprietary content, or internal data.

Mitigation: Manually review skill folders before publish or sync, exclude `.env` files, tokens, keys, credentials, internal URLs, customer data, and other proprietary artifacts.

Risk: Token-based login commands can leak credentials if real tokens are pasted into commands or support transcripts.

Mitigation: Use interactive `clawhub login` where possible and avoid sharing real API tokens in command examples, logs, or troubleshooting output.

## Reference(s):

- [ClawHub CLI Commands](reference/CLI-COMMANDS.md)
- [Publishing Checklist](reference/PUBLISHING-CHECKLIST.md)
- [Security and Safety](reference/SECURITY.md)
- [SemVer Guide](reference/SEMVER-GUIDE.md)
- [Skill Package Structure](reference/SKILL-STRUCTURE.md)
- [Troubleshooting](reference/TROUBLESHOOTING.md)
- [Windows Usage](reference/WINDOWS-USAGE.md)
- [ClawHub skill page](https://clawhub.ai/openlang-cn/skills/clawhub-cli)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands should be adapted after checking local ClawHub CLI help when flags are uncertain.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

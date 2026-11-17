## Description:

Stop leaking secrets. Pre-commit hooks + 10-point scans + cron monitoring. Agent-ops security in one command. By The Agent Wire (theagentwire.ai)

This skill is ready for commercial/non-commercial use.

## Publisher:

[theagentwire](https://clawhub.ai/user/theagentwire)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to add pre-commit secret scanning, repository security checks, and cron-friendly monitoring to local projects. It is aimed at reducing accidental credential leaks in agent-assisted development workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default scans can inspect shell profiles, home-directory .env files, SSH configuration, open ports, and other workstation-level data.

Mitigation: Review the scan scope before installation and run it only in environments where that inspection is intended.

Risk: Scan reports may include full lines containing secrets, credential-like strings, file paths, listening ports, or other host metadata.

Mitigation: Redact reports before sharing, storing, or running in CI and cron workflows.

Risk: The setup command can install or update a pre-commit hook and append security patterns to .gitignore.

Mitigation: Run setup in a version-controlled repository, review hook and .gitignore changes, and keep CI-side scanning as backup for commits made with --no-verify.

Risk: The --fix-ssh option changes SSH directory, key, and config file permissions.

Mitigation: Use --fix-ssh only when permission changes are intentional and compatible with the local SSH setup.

## Reference(s):

- [Secret Patterns Reference](references/patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/theagentwire/skills/agent-security-ops)
- [Publisher Profile](https://clawhub.ai/user/theagentwire)
- [The Agent Wire](https://theagentwire.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON scan reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Setup changes repository hook and ignore-file configuration; scan and monitor commands emit human-readable summaries and JSON reports.]

## Skill Version(s):

1.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

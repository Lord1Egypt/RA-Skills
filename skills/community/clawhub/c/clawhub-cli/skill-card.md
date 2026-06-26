## Description: <br>
Use the ClawHub CLI to search, install, update, and publish agent skills from clawhub.ai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlang-cn](https://clawhub.ai/user/openlang-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to produce concise ClawHub CLI command guidance for discovering, installing, updating, publishing, and syncing agent skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk sync can publish skill folders and may run without a dry run if the installed ClawHub CLI does not support the requested dry-run flag. <br>
Mitigation: Confirm CLI support with `clawhub sync --help`, manually review the generated command, and avoid `scripts/linux/sync-all.sh --dry-run` unless dry-run support is confirmed. <br>
Risk: Publishing or syncing skill folders can expose secrets, credentials, private keys, internal URLs, customer data, logs, or proprietary files. <br>
Mitigation: Review the folder tree before publish or sync, exclude sensitive files, and use least-privilege credentials. <br>
Risk: Passing tokens on the command line can expose credentials through shell history or process listings. <br>
Mitigation: Prefer interactive login or a safer credential flow where available, and avoid command-line tokens when possible. <br>


## Reference(s): <br>
- [Clawhub Cli skill page](https://clawhub.ai/openlang-cn/clawhub-cli) <br>
- [CLI Commands](reference/CLI-COMMANDS.md) <br>
- [Publishing Checklist](reference/PUBLISHING-CHECKLIST.md) <br>
- [Security & Safety](reference/SECURITY.md) <br>
- [Troubleshooting](reference/TROUBLESHOOTING.md) <br>
- [Windows Usage](reference/WINDOWS-USAGE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ClawHub CLI commands, SemVer guidance, preflight checks, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

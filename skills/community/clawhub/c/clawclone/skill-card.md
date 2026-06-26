## Description: <br>
ClawClone backs up, uploads, downloads, shares, and restores OpenClaw workspace state across local and cloud locations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawclone-cc](https://clawhub.ai/user/clawclone-cc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create local or cloud backups, migrate an OpenClaw workspace to another instance, share agent configurations, and preview or restore saved OpenClaw state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups may contain credentials, tokens, memory, agent files, settings, scripts, cron data, and other sensitive OpenClaw state. <br>
Mitigation: Use local export for sensitive workspaces, inspect what will be included, and rotate credentials if a sensitive backup was uploaded or shared unintentionally. <br>
Risk: Cloud uploads and share links can expose secret-bearing backup archives beyond the local environment. <br>
Mitigation: Avoid share links for backups containing secrets, revoke shares when they are no longer needed, and limit cloud use to data the user intends to store remotely. <br>
Risk: Restore and clone operations can modify or overwrite OpenClaw workspace state. <br>
Mitigation: Run clone or import with --test first, review the generated report, and proceed only after confirming the target backup and expected file changes. <br>


## Reference(s): <br>
- [ClawClone ClawHub listing](https://clawhub.ai/clawclone-cc/clawclone) <br>
- [ClawClone service](https://clawclone.cc) <br>
- [ClawClone API key settings](https://clawclone.cc/dashboard/settings) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent to create, upload, download, verify, share, revoke, or restore OpenClaw backup archives.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

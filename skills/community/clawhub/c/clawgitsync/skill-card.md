## Description: <br>
clawsync helps agents back up, migrate, restore, and serve OpenClaw state using Git-native sync, local archives, secret sanitization, and safe restore defaults. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linsheng9731](https://clawhub.ai/user/linsheng9731) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to back up OpenClaw state, migrate it between machines, restore from Git branches or local archives, run periodic backups, prune remote backup branches, and serve archives through a token-protected local service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install flow can run a remote shell script while the skill requests access to sensitive OpenClaw state. <br>
Mitigation: Review the installer and CLI source before installation, prefer a pinned release or locally inspected install, and install only from a trusted source. <br>
Risk: Backups and archives may contain sensitive OpenClaw data such as credentials, sessions, and configuration. <br>
Mitigation: Keep remotes and archive locations private, use the documented sanitization workflow, and review backup scope before sharing or syncing archives. <br>
Risk: Restore, pull, merge, and pruning operations can overwrite or remove important local state. <br>
Mitigation: Run dry-runs first, review the high-risk paths summary, rely on pre-restore snapshots, and apply changes only after explicit confirmation. <br>
Risk: The token-protected archive server could expose backup archives if made public without additional controls. <br>
Mitigation: Keep the service local or private, protect tokens, and use TLS with a trusted reverse proxy before any public exposure. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/linsheng9731/clawgitsync) <br>
- [GitHub installer script](https://raw.githubusercontent.com/linsheng9731/clawsync/main/scripts/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes dry-run, confirmation, backup, restore, pruning, and token-protected serving guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

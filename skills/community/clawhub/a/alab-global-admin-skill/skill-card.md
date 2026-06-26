## Description: <br>
Use when administering an ALab home with root authority, including home bootstrap, root and project-admin credential management, project initialization and handoff, SkyDiscover catalog management, global cache or backup pruning, and root-level audit/dashboard inspection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bebetterest](https://clawhub.ai/user/bebetterest) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
ALab home administrators use this skill for root-scoped setup, credential rotation, project initialization and handoff, catalog lifecycle work, cleanup, and audit or dashboard inspection. It is intended for privileged administration, not routine project coordination or experiment work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Root and project-admin credentials could be exposed through prompts, logs, command history, screenshots, reports, or tracked files. <br>
Mitigation: Keep keys out of prompts and logs; prefer stdin, ignored local secret files, private environment variables, or an approved secure store. <br>
Risk: Root-level cleanup, credential revocation, catalog removal, or project removal can disrupt active ALab work. <br>
Mitigation: Use dry-runs where available, verify key ids and project scope, review audit events and blockers, and require explicit confirmation before destructive actions. <br>
Risk: Delegating root authority or broad credentials to lower-layer work can expand privilege beyond the task. <br>
Mitigation: Delegate only the credential needed for the specific project or worktree, and hand project work to the appropriate lower-layer ALab skill. <br>
Risk: The local dashboard can expose hidden logs, full logs, artifacts, or token URLs if shared outside the root-admin session. <br>
Mitigation: Use the dashboard only for local read-only inspection, keep it bound locally, and do not share the token URL. <br>


## Reference(s): <br>
- [ALab Global Admin Commands](references/commands.md) <br>
- [ALab Global Admin Commands (Chinese)](references/commands_cn.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance emphasizes least-privilege handoff, secure credential handling, dry-runs for destructive actions, and local-only dashboard inspection.] <br>

## Skill Version(s): <br>
0.1.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

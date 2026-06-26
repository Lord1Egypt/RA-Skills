## Description: <br>
Repairs local Codex Desktop history indexes so migrated or restored sessions appear in the sidebar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lttcnly](https://clawhub.ai/user/lttcnly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Codex Desktop users use this skill when local sessions exist on disk but are hidden from the sidebar after migration or restore. It guides a dry-run-first repair of Codex state files, rollout metadata, history indexes, and sidebar project assignments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The repair can rewrite sensitive local Codex state, history indexes, rollout metadata, and project assignments. <br>
Mitigation: Run with --dry-run first, review the reported changes, close Codex Desktop before applying when possible, and keep the generated backup directory private. <br>
Risk: When Codex Desktop is running, the script can launch hidden deferred PowerShell helpers to reapply global state after the app exits. <br>
Mitigation: Prefer closing Codex Desktop before applying the repair, avoid broad --scan-project-parent and --protect-state-minutes use, and inspect or remove deferred scripts from the backup directory after completion. <br>
Risk: The app-server verification path starts Codex with analytics enabled by default. <br>
Mitigation: Skip --verify-app-server if that verification path is not acceptable, and rely on dry-run output plus manual sidebar checks instead. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lttcnly/codex-history-visibility-repair) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, JSON] <br>
**Output Format:** [Markdown guidance with PowerShell commands and JSON repair summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script can create local backups and emits counts for selected threads, visible threads, project mappings, pruned roots, provider distribution, and verification results.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

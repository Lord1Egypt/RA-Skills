## Description: <br>
Standardized instructions for installing, structuring, and configuring custom skills for AI-powered IDEs and editors, including multi-IDE migration, global and project skill setup, OpenClaw configuration, and release preparation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luckycat133](https://clawhub.ai/user/luckycat133) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, install, migrate, synchronize, verify, and publish custom agent skills across supported AI IDEs and CLI tools. It is especially relevant for teams standardizing shared skill directories, OpenClaw setup, or migration workflows between agent environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled migration and sync helpers can persistently rewrite or delete skill and configuration files across multiple IDE environments. <br>
Mitigation: Run dry-run or preview modes first, verify every source and target path, keep backups, and avoid overwrite or mirror-delete behavior unless removals are intended. <br>
Risk: OpenClaw automation may install software, run remote installers, install metadata-declared dependencies, and update persistent OpenClaw configuration. <br>
Mitigation: Use the OpenClaw auto-config helper only in high-trust environments, verify installer and dependency sources before execution, and use skip-install or skip-doctor options when a non-intrusive configuration pass is required. <br>
Risk: Migration reports and generated configuration may still require target-IDE-specific manual follow-up. <br>
Mitigation: Review post-migration steps for the target IDE, restart or reload the IDE where required, and run the bundled verification helper before treating the migration as complete. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/luckycat133/agent-skills-setup) <br>
- [Antigravity Skills Reference](references/antigravity.md) <br>
- [Claude Code Skills Reference](references/claude-code.md) <br>
- [OpenAI Codex Skills Reference](references/codex.md) <br>
- [IDE Configuration Verification](references/ide-config-verification.md) <br>
- [IDE Migration Reference](references/ide-migration.md) <br>
- [OpenClaw Skills Reference](references/openclaw.md) <br>
- [Publishing Reference](references/publishing.md) <br>
- [Trae Skills Reference](references/trae.md) <br>
- [VS Code Copilot Skills Reference](references/vscode-copilot.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, file paths, configuration snippets, and migration reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce dry-run previews, migration reports, verification summaries, release commands, and configuration edits.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

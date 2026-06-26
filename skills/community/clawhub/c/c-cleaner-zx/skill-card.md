## Description: <br>
Windows C Drive Cleaner helps agents scan and report on C drive usage, identify cleanup candidates, and perform user-confirmed cleanup or migration actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zx0018](https://clawhub.ai/user/zx0018) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and IT operators use this skill to inspect Windows C drive space, review cleanup candidates, and carry out file cleanup or migration only after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires credentials and network access to inspect a Windows host through WinRM. <br>
Mitigation: Use secure credential storage, prefer WinRM over HTTPS, restrict access to trusted sources, and avoid plaintext credential files. <br>
Risk: Migration can copy files from the Windows host to the agent server. <br>
Mitigation: Set MIGRATION_TARGET only when file export is intended, confirm the destination before migration, and use scan-only mode when files should remain on the Windows host. <br>
Risk: Cleanup actions can delete or move files if approved incorrectly. <br>
Mitigation: Review each proposed delete, move, deduplication, or migration action before confirming, and keep protected paths whitelisted. <br>
Risk: Ignoring server certificate validation can weaken WinRM transport security. <br>
Mitigation: Change certificate validation to a trusted and verified mode before using the skill in sensitive environments. <br>


## Reference(s): <br>
- [Path Assumptions](references/path-assumptions.md) <br>
- [Safety Rules](references/safety-rules.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zx0018/c-cleaner-zx) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, confirmation prompts, configuration snippets, and PowerShell or shell command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operations that delete, move, or migrate files are expected to require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

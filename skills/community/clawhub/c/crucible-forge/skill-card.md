## Description:

Crucible Forge helps AI agent users scan local workspaces, generate human-reviewable reorganization plans, and run pre/post audits for file integrity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI agent operators use this skill to assess file-based workspaces, plan safer reorganizations, and audit whether protected files, references, backups, and file counts remain intact. It is most relevant for workspace cleanup, migration preparation, team standardization, and post-incident review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Executable Python configuration files can run arbitrary code when loaded.

Mitigation: Use only configuration files you authored or fully reviewed, and do not run the tools with elevated privileges.

Risk: Broad local workspace analysis and process checks can inspect sensitive files, paths, and commands.

Mitigation: Run the skill only in trusted workspaces you own, configure protected files and directories, and review generated reports before sharing them.

Risk: Generated plans and audits are advisory and may overstate safety or miss data-loss scenarios.

Mitigation: Verify independent backups before moving files, manually review every plan, execute changes deliberately, and run pre/post audits during quiet periods.

Risk: Symlinks, binary references, concurrent writes, very long paths, and naming conflicts can produce incomplete or misleading results.

Mitigation: Check known edge cases from the limitations document, resolve conflicts manually, and verify important references and symlinks after any reorganization.

## Reference(s):

- [Crucible Forge on ClawHub](https://clawhub.ai/theshadowrose/skills/crucible-forge)
- [Publisher profile](https://clawhub.ai/user/theshadowrose)
- [README](artifact/README.md)
- [Limitations](artifact/LIMITATIONS.md)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, Python configuration, JSON scan reports, JSON reorganization plans, audit reports, and rollback shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operates on local workspace files and produces advisory plans and audit findings for human review.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact frontmatter states 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
